# Utils

## Table of contents

1. [classproperty](#classproperty)
2. [DecoratorInjector](#decoratorinjector)
3. [LoggerBase](#loggerbase)
4. [annotatable](#annotatable)
5. [Interface](#interface)

## classproperty

Analog of `property` for a class without instantiation. No `setter` or `deleter`

### Usage

```python
from agutilg import classproperty

class MyClass:

    @classproperty
    def prop(cls):
        return 'Some value'

value = MyClass.prop
```

## DecoratorInjector

Used to wrap all methods of a class in a list of decorators

### Usage

```python
from agutils import DecoratorInjector


def d1(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def d2(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

DecoratorInjector(d1, d2)
class MyClass:...

```

## LoggerBase

Class for configuring a logger without creating an instance.

### Usage

Inherit the LoggerBase class:

```python
class MainLog(LoggerBase):...
```

After this you can call the class anywhere:

```python
MainLog.debug('Test message')
```

To configure, define the `Config` class inside (see `DefaultConfig` in `LogMeta`)

```python
class MainLog(LoggerBase):
    class Config:
        level = DEBUG
        handlers = [
            StreamHandler(stdout),
            FileHandler('test.log')
        ]
        fmt = Formatter(
            style='{',
            datefmt='%Y:%m:%d %H:%M:%S',
            fmt='{LoggerName} - {asctime} - {levelname} - {message}'
        )
```

To use the logger name, use the variable `LoggerName`

## annotatable

The decorator will find all `Annotated[Type, GeneratorMethod]` arguments and if no value is passed for them when called or the value does not match the `Type`, it will fill it with the value obtained from `GeneratorMethod`

### Usage

```python
def get_session() -> Session:
    return Session(engine)

SessionT = Annotated[Session, get_session]

@annotatable
def get_user(id:int, sess:SessionT) -> User:
    return sess.execute(
        select(User).where(User.id == 1)
    ).first()
```

We can pass a session object to the call

```python
user = get_user(id=1, sess=get_session())
```

Or we can not pass it. Then the function will be passed the result of the `get_session` function specified in the `SessionT` metadata

```python
user = get_user(id=1)
```

Good to use with DecoratorInjector

```python
from agutils import DecoratorInjector, annotatable

@DecoratorInjector(annotatable)
class Helper:

    @staticmethod
    def get_session() -> Session:
        return Session(bind=engine)

    SessionT = Annotated[Session, get_session]


    def get_user(self, id:int, sess:SessionT) -> User:...

    def get_users(self, sess:SessionT) -> list[User]:...

```

## Interface

Decorator for declaring a class as an Interface.
**For interface**: checks for missing method implementations, saves method signatures.
**For implementation**: checks for method implementation, method signatures match.
The implementation of an interface is the first class that inherits the interface.

To view the interface description, you can pass it to the `print` function or call the `__description__()` method.

### Usage

```python
from agutils import Interface

@Interface
class IPerson:
    def get_name(self) -> str:...
    def get_age(self) -> int:...

```

Alternative interface declaration

```python
from agutils import Interface


class Person:
    def get_name(self) -> str:...
    def get_age(self) -> int:...

IPerson = Interface[Person]

```

#### Show description

`IPerson.__description__(prnt=True)` or `print(IPerson)` will display the following information

```shell

IPerson[Interface]
Methods:

  1. def get_name(self) -> str:...
  2. def get_age(self) -> int:...

```

If you call a description for an implementation class or its descendants, the implementation flag will be added to the interface name.

```python
class User(IPerson):
    def get_name(self) -> str:
        return self.name
    def get_age(self) -> int:
        return self.age

print(User)
```

Output:

```shell

IPerson[Interface] (implemented)
Methods:

  1. def get_name(self) -> str:...
  2. def get_age(self) -> int:...

```

If a class implements several interfaces, information on each interface will be displayed.
