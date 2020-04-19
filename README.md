# pyMonet

[![Build Status](https://travis-ci.org/przemyslawjanpietrzak/pyMonet.svg?branch=develop)](https://travis-ci.org/przemyslawjanpietrzak/pyMonet)
[![Coverage Status](https://coveralls.io/repos/github/przemyslawjanpietrzak/pyMonet/badge.svg?branch=develop)](https://coveralls.io/github/przemyslawjanpietrzak/pyMonet?branch=develop)
[![Documentation Status](https://readthedocs.org/projects/pymonet/badge/?version=develop)](https://pymonet.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/pymonet.svg)](https://badge.fury.io/py/pymonet)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

High abstract python library for functional programming.
Contains algebraic data structures known (or unknown) from Haskell or Scala.
With MIT licence. [Docs](http://pymonet.readthedocs.io/en/latest/?badge=latest)


# Install:
`pip install pymonet`


# Content:

### [Either](#either-1)
The Either type represents values with two possibilities: B value of type Either<A, B> is either Left<A> or Right. But not both in the same time.
### [Maybe](#maybe-1)
Maybe type is the most common way of representing nothingness (or the null type).
Maybe is effectively abstract and has two concrete subtypes: Box (also Some) and Nothing.
### [Box](#box-1)
Boxs are data-types that store values. No restriction is placed on how they store these values, though there may be restrictions on some methods if a Box is also an instance of a sub-class of Box.
### [Semigroups](#semigroups-1)
In mathematics, a semigroup is an algebraic structure consisting of a set together with an associative binary operation.
A semigroup generalizes a monoid in that there might not exist an identity element.
It also (originally) generalized a group (a monoid with all inverses) to a type where every element did not have to have an inverse, this the name semigroup.
### [Lazy](#lazy-1)
Lazy are data-types that store functions. Stored function will not be called until call of bind method
### [ImmutableList](#immutable-list-1)
Implementation of list data structures with immutable methods
### [Task](#task-1)
Task are data-type for handle execution of functions (in lazy way) transform results of this function and handle errors.
### [Try](#try-1)
The Try control gives us the ability write safe code without focusing on try-catch blocks in the presence of exceptions.
### [Validation](#Validation-1)
It that can hold either a success value or a failure value and has methods for accumulating errors.
### [Utils](#utils-1)
Set of functional programming helpers

## Either
The Either type represents values with two possibilities: B value of type Either<A, B> is either Left<A> or Right. But not both in the same time.
Left represents error value so any maps and bind will NOT be applied on it.

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
    .bind(lambda value: Right(value + 1))
    .case(error=handle_error, success=handle_success))
# error 42

(divide(42, 1)
    .map(identity, lambda value: value + 1)
    .bind(lambda value: Right(value + 1))
    .case(error=handle_error, success=handle_success))
# success  44
```


## Maybe
Maybe type is the most common way of representing nothingness (or the null type) with making the possibilities of NullPointer issues disappear.
Maybe is effectively abstract and has two concrete subtypes: Some (also Box) and None (also Nothing).


```python
from pymonet.Maybe import Maybe


def get_index(item):
    if item in [1,2,3]:
        return Maybe.just(42)
    return Maybe.nothing()

get_index(42).get_or_else(0)  # 0
get_index(1).get_or_else(0)  # 3

```

bind and map methods will be applied only when maybe is not empty
```python
from pymonet.Maybe import Maybe


get_index(42)\
  .map(lambda value: value + 1)\
  .bind(lambda value: Maybe.just(value + 1))\
  .get_or_else(0)
# 0

get_index(1)\
  .map(lambda value: value + 1)\
  .bind(lambda value: Maybe.just(value + 1))\
  .get_or_else(0)
# 3
```

Filter method will be applied on maybe value and return it with or without value, depend on filter result:
```python
from pymonet.Maybe import Maybe


get_index(42)\
    .filter(lambda value: value % 2 == 0)\
    .get_or_else(0)
# 0

get_index(3)\
    .filter(lambda value: value % 2 == 0)\
    .get_or_else(0)
# 0

get_index(2)\
    .filter(lambda value: value % 2 == 0)\
    .get_or_else(0)
# 2
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
    .bind(lambda value: "output = " + value))  # "output = 34"
```

## Semigroups
In mathematics, a semigroup is an algebraic structure consisting of a set together with an associative binary operation.
A semigroup generalizes a monoid in that there might not exist an identity element.
It also (originally) generalized a group (a monoid with all inverses) to a type where every element did not have to have an inverse, this the name semigroup.

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

Sum(42).bind(lambda value: value)  # 42
```

#### First
```python
from pymonet.semigroups import First

First('first').concat(First('Second'))  # First<"first">
First('first').bind(lambda value: value[::-1])  # "tsrif"
```

#### Map
```python
from pymonet.semigroups import Sum, All, First, Map
ingredient1 = Map({'score': Sum(1), 'won': All(True), 'captain': First('captain america')})
ingredient2 = Map({'score': Sum(2), 'won': All(True), 'captain': First('iron man')})
ingredient1.concat(ingredient2)  # Map<{'score': Sum(3), 'won': All(True), 'captain': First('captain america')}>
```

## Lazy
Lazy are data-types that store functions. Stored function will not be called until call of bind method
```python
from pymonet.lazy import Lazy

def fn():
    print('fn call')
    return 42

def mapper(value):
    print('mapper side effect of ' + value)
    return value + 1

def side_effect(value):
    print('side effect of ' + value)

lazy = Lazy(fn)
mapped_lazy = lazy.map(mapper)
mapped_lazy.bind(side_effect)  
# fn call
# mapper side effect of 42
# side effect of 42
```
Lazy instances memoize output of constructor function
```python
lazy = Lazy(fn)
value1 = lazy.get()
# fn call
value2 = lazy.get()
print(value1, value2)
# 42, 42
```

## ImmutableList
Implementation of list data structures with immutable methods
```python
lst = ImmutableList.of(1, 2, 3)

lst.map(increase) # ImmutableList.of(2, 3, 4)
lst.filter(lambda item: item % 2 == 0) # ImmutableList.of(2)
lst.find(lambda item: item % 2 == 0) # 2
lst.map(increase) # ImmutableList.of(2, 3, 4)
lst.reduce(lambda acc, curr: acc + curr, 0) # 6
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
map method will be applied only on resolvable tasks during calling bind method
```python
resolvable_task.map(lambda value: value + 1)  # Task<() -> 43>
rejectable_task.map(lambda value: value + 1)  # Task<() -> 0>
```
bind method will be applied only on resolvable tasks. bind also will call stored function
```python
def mapper(value):
    print('mapper side effect ' + value)
    return value + 1

resolvable_task.bind(mapper)
# resolve side effect
# mapper side effect 42

rejectable_task.bind(mapper)
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

## Validation
It that can hold either a success value or a failure value and has methods for accumulating errors
```python
from pymonet.validation import Validation


def test_validation_is_fail():
    assert Validation.fail(['fail']).is_fail()


def validate_length(value):
    if len(value) < 5:
        return Validation.fail(['value not long enough'])
    return Validation.success()


def validate_uppercase(value):
    if value[0].upper() != value[0]:
        return Validation.fail(['value not uppercase'])
    return Validation.success()


def validate_contains_special_character(value):
    if re.match(r'^[a-zA-Z0-9_]*$', value):
        return Validation.fail(['value not contains special character'])
    return Validation.success()


def validate(value):
    return (Validation.success(value)
            .ap(validate_length)
            .ap(validate_uppercase)
            .ap(validate_contains_special_character))


validate('Success$') # Validation['Success$', []]
validate('Success') # Validation['Success$', ['value not uppercase']]
validate('S$') # Validation['Success$', ['value not long enough']]
validate('s$') # Validation['Success$', ['value not long enough', 'value not uppercase']]
validate('s') # Validation['Success$', ['value not long enough', 'value not uppercase', 'value not contains special character']]
```


## Utils
#### compose
Compose: performs right-to-left function composition.
```python
from pymonet.utils import \
    increase,\
    compose,\
    curried_map as map,\
    curried_filter as filter

compose(
    list(range(10)),
    map(increase),
    filter(is_odd)
)
#[1, 3, 5, 7, 9]
```
#### pipe
Pipe: performs left-to-right function composition.
```python
from pymonet.utils import increase, pipe

pipe(42, increase, lambda value: value * 2)
#86
```
#### cond
Returns a function which encapsulates if/else, if/else, ... logic. cond takes a list of (predicate, transformer) pairs. All of the arguments to fn are applied to each of the predicates in turn until one returns a truthy value, at which point fn returns the result of applying its arguments to the corresponding transformer.
```python
from pymonet.utils import cond

fn = cond([
    (lambda arg: arg == 0, lambda: 'first'),
    (lambda arg: arg == 1, lambda: 'second'),
    (lambda arg: arg == 2, lambda: 'third').
])
fn(1) #  second
# lambda arg: arg == 2 will not be call
```

#### memoize
Creates a new function that, when invoked,
caches the result of calling fn for a given argument set and returns the result.
Subsequent calls to the memoized fn with the same argument set will not result in an additional call to fn;
instead, the cached result for that set of arguments will be returned.

```python
from pymonet.utils import memoize, eq

def fn(arg):
    print('fn flag')
    return arg + 1

memoized_fn = memoize(fn)
memoized_fn(42) # 43
# fn flag

memoized_fn(42) # 43
# print to called

memoized_fn(43) # 44
# fn flag

```