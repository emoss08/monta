<h3 align="center">Monta Type Annotations</h3>

------------------------------------------------------------------------

## Introduction

Type annotations are a way to add type information to Python code. They are
intended to be used by static type checkers to help find bugs in your code.
Type checkers can also use type annotations to provide better code
completion and other features.

Type annotations are specified using a syntax that is similar to the
syntax for type hints, but with a few differences. The syntax for
annotations is described in the [PEP 484](https://www.python.org/dev/peps/pep-0484/)

## Type Annotations in Monta

Monta uses type annotations to provide type checking for the entire
application. This is done using the [mypy](http://mypy-lang.org/) type
checker. Mypy is a third-party tool that is not included in the Python
standard library.

Type annotations are used in the following ways:

-   Type annotations are used to specify the type of function arguments
    and return values.
-  Type annotations are used to specify the type of class attributes.
-  Type annotations are used to specify the type of variables.

## Examples

### Function Arguments and Return Values

```python
def add(a: int, b: int) -> int:
    return a + b
```

### Class Attributes

```python
class User:
    name: str
    age: int
```

### Variables

```python
name: str = "John"
age: int = 30
```

## Monta Types

Monta uses the following types:

- path: django/http/request.pyi
```python
user: Union[AbstractBaseUser, AnonymousUser, MontaUser] = ...
```