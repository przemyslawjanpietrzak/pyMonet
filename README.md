# pyMonet

[![Build Status](https://travis-ci.org/przemyslawjanpietrzak/pyMonet.svg?branch=master)](https://travis-ci.org/przemyslawjanpietrzak/pyMonet)

High abstract python library for functional programming.
Contains algebraic data structures known (or unknown) from Haskell or Scala.
With MIT licence.


# Install:
`pip install pymonet`


# Content:

### [Either](#either-1)
The Either type represents values with two possibilities: B value of type Either<A, B> is either Left<A> or Right. But not both in the same time.
### [Box](#box-1)
Boxs are data-types that store values. No restriction is placed on how they store these values, though there may be restrictions on some methods if a Box is also an instance of a sub-class of Box.
### [Semigroups](#semigroups-1)
In mathematics, a semigroup is an algebraic structure consisting of a set together with an associative binary operation.
A semigroup generalizes a monoid in that there might not exist an identity element.
It also (originally) generalized a group (a monoid with all inverses) to a type where every element did not have to have an inverse, thus the name semigroup.
### [Applicative](#applicative-1)
Applicative are data-types that store functions. Stored function will not be called until call of fold method
### [Task](#task-1)
Task are data-type for handle execution of functions (in lazy way) transform results of this function and handle errors.
### [Try](#try-1)
The Try control gives us the ability write safe code without focusing on try-catch blocks in the presence of exceptions.

## Either
The Either type represents values with two possibilities: B value of type Either<A, B> is either Left<A> or Right. But not both in the same time.
Left represents error value so any maps and fold will NOT be applied on it.

```python
from pymonet.either import Left, Right
from pymonet.utils import identity

def divide(divided, divider):
    if divider == 0:
        return Left('can not divide by 0')
    return Right(divided, divider)

def handle_error(value):
    print ('error {}'.format(value))

def handle_success(value):
    print ('success {}'.format(value))

(divide(42, 0)
    .map(lambda value: value + 1)
    .fold(lambda value: Right(value + 1))
    .case(error=handle_error, success=handle_success))
# error 42

(divide(42, 1)
    .map(identity, lambda value: value + 1)
    .fold(lambda value: Right(value + 1))
    .case(error=handle_error, success=handle_success))
# success  44
```

## Box
Boxs are data-types that store values. No restriction is placed on how they store these values, though there may be restrictions on some methods if a Box is also an instance of a sub-class of Box.
```python
from pymonet.box import Box
box = Box(42)  # Box<42>
(box
    .map(lambda value: value + 1)  # Box<43>
    .map(lambda value: str(value))  # Box<"43">
    .map(lambda value: value[::-1])  # Box<"34">
    .fold(lambda value: "output = " + value))  # "output = 34"
```

## Semigroups
In mathematics, a semigroup is an algebraic structure consisting of a set together with an associative binary operation.
A semigroup generalizes a monoid in that there might not exist an identity element.
It also (originally) generalized a group (a monoid with all inverses) to a type where every element did not have to have an inverse, thus the name semigroup.

#### All
```python
from pymonet.semigroups import All

All(True).concat(All(False))  # All<False>
All(True).concat(All(True))  # All<True>
```

== operator compares value of semigroups
```python
All(True) == All(True)  # True
All(True) == All(False)  # False
```

#### Sum
```python
from pymonet.semigroups import Sum

Sum(42).concat(Sum(1))  # Sum<43>
Sum(42).concat(Sum(1)).concat(Sum(1))  # Sum<44>
Sum(42).concat(Sum(1).concat(Sum(1)))  # Sum<44>

Sum(42).fold(lambda value: value)  # 42
```

#### First
```python
from pymonet.semigroups import First

First('first').concat(First('Second'))  # First<"first">
First('first').fold(lambda value: value[::-1])  # "tsrif"
```

#### Map
```python
from pymonet.semigroups import Sum, All, First, Map
ingredient1 = Map({'score': Sum(1), 'won': All(True), 'captain': First('captain america')})
ingredient2 = Map({'score': Sum(2), 'won': All(True), 'captain': First('iron man')})
ingredient1.concat(ingredient2)  # Map<{'score': Sum(3), 'won': All(True), 'captain': First('captain america')}>
```

## Applicative
Applicative are data-types that store functions. Stored function will not be called until call of fold method
```python
from pymonet.applicative import Applicative

def fn():
    print('fn call')
    return 42

def mapper(value):
    print('mapper side effect of ' + value)
    return value + 1

def side_effect(value):
    print('side effect of ' + value)

applicative = Applicative(fn)
mapped_applicative = applicative.map(mapper)
mapped_applicative.fold(side_effect)  
# fn call
# mapper side effect of 42
# side effect of 42
```


## Task
Task are data-type for handle execution of functions (in lazy way) transform results of this function and handle errors.
```python
from pymonet.task import Task

def resolvable_fn(reject, resolve):
    print('resolve side effect')
    resolve(42)

def rejectable_fn(reject, resolve):
    print('reject side effect')
    reject(0)

resolvable_task = Task.of(resolvable_fn)
rejectable_task = Task.of(rejectable_fn)
```
map method will be applied only on resolvable tasks during calling fold method
```python
resolvable_task.map(lambda value: value + 1)  # Task<() -> 43>
rejectable_task.map(lambda value: value + 1)  # Task<() -> 0>
```
fold method will be applied only on resolvable tasks. Fold also will call stored function
```python
def mapper(value):
    print('mapper side effect ' + value)
    return value + 1

resolvable_task.fold(mapper)
# resolve side effect
# mapper side effect 42

rejectable_task.fold(mapper)
# reject side effect
```

## Try
The Try control gives us the ability write safe code without focusing on try-catch blocks in the presence of exceptions.
```python
from pymonet.monad_try import Try

def divide(dividend, divisor):
    return dividend / divisor

def success_callback(value):
    print('success: {}'.format(value))

def fail_callback(error):
    print('error: {}'.format(value))

(Try.of(divide, 42, 2)
    .on_success(success_callback)
    .on_fail(fail_callback))
# success: 21

(Try.of(divide, 42, 0)
    .on_success(success_callback)
    .on_fail(fail_callback))
#error: division by zero
```
map method will be only applied mapper when exception was not thrown
```python
(Try.of(divide, 42, 2)
    .map(lambda value: value + 1)
    .on_success(success_callback)
    .on_fail(fail_callback))
# success: 22

(Try.of(divide, 42, 0)
    .on_success(success_callback)
    .map(lambda value: value + 1)
    .on_fail(fail_callback))
#error: division by zero
```
get_or_else method returns value when exception was not thrown
```python
Try.of(divide, 42, 2).get_or_else('Holy Grail') # 21
Try.of(divide, 42, 0).get_or_else('Holy Grail') # 'Holy Grail'
```

get method should return value with or without exception thrown
```python
Try.of(divide, 42, 2).get()  # 21
Try.of(divide, 42, 0).get()  # ZeroDivisionError<'division by zero'>
```
