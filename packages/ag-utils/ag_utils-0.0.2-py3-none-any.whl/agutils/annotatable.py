from dataclasses import dataclass
from functools import update_wrapper
from inspect import getfullargspec
from typing import (Annotated, Callable, Dict, Generic, List, ParamSpec, Tuple,
                    TypeVar, get_args, get_origin)

T = TypeVar('T')
P = ParamSpec('P')


class annotatable(Generic[T]):

    """
    The decorator will find all `Annotated[Type, GeneratorMethod]` arguments and if no value is passed for them when called or the value does not match the `Type`, it will fill it with the value obtained from `GeneratorMethod`

    ```
    def get_session() -> Session:
        return Session(engine)

    SessionT = Annotated[Session, get_session]

    @annotatable
    def get_user(id:int, sess:SessionT):...

    ```
    Now, if we don't pass a `Session` object to the function, the object will be created by calling the `get_session()` method.
    ```
    user = get_user(id=1)
    ```

    An argument with an `Annotated` type can appear anywhere in the function declaration and can be passed as either a positional or named argument.
    All metadata in `Annotated` except the first element is ignored and can be used for other purposes. The first element must be a default value generator.
    """

    @dataclass
    class ArgsKwargs:
        args:Tuple
        kwargs:Dict

    @dataclass
    class Kwarg:
        name:str
        pos:int
        t:type
        generator:Callable

    __akwargs:List[Kwarg]

    def __init__(self, func:Callable[P, T]) -> Callable[P, T]:
        if not callable(func):
            raise ValueError("Func must be callable. Are you sure you are using class as a decorator?")
        update_wrapper(self, func)
        self.__func = func
        self.__gen_akwargs()

    def __gen_akwargs(self) -> None:
        self.__akwargs = []
        argspec = getfullargspec(self.__func)
        for i, arg in enumerate(argspec.args):
            annot = argspec.annotations.get(arg, None)
            if not annot: continue
            if get_origin(annot) is Annotated:
                t = get_args(annot)[0]
                meta = annot.__metadata__[0]
                if callable(meta):
                    self.__akwargs.append(
                        self.Kwarg(
                            name=arg, pos=i, t=t, generator=meta
                        )
                    )
        if len(argspec.args) > 0 and argspec.args[0] == 'self':
            for akwarg in self.__akwargs:
                akwarg.pos -= 1

    def __process_func_args(self, argkw:ArgsKwargs) -> ArgsKwargs:
        for akwarg in self.__akwargs:
            if akwarg.pos < 0: continue

            kw = argkw.kwargs.get(akwarg.name, None)
            if kw:
                if not isinstance(kw, akwarg.t):
                    argkw.kwargs.update({akwarg.name: akwarg.generator()})
            else:
                if len(argkw.args) >= (akwarg.pos+1):
                    if not isinstance(argkw.args[akwarg.pos], akwarg.t):
                        argkw.args = argkw.args[:akwarg.pos] + (akwarg.generator(),) + argkw.args[akwarg.pos+1:]
                else:
                    argkw.kwargs.update({akwarg.name: akwarg.generator()})
        return argkw

    def __call__(self, *args:P.args, **kwargs:P.kwargs) -> T:
        result = self.__process_func_args(self.ArgsKwargs(args, kwargs))
        return self.__func(*result.args, **result.kwargs)