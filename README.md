# monet.py

[![Build Status](https://travis-ci.org/przemyslawjanpietrzak/MonetPy.svg?branch=master)](https://travis-ci.org/przemyslawjanpietrzak/MonetPy)

High abstract python library for functional programming.
Contains algebraic data structures known (or unknown) from Haskell or Scala.
With MIT licence.
 
 
# Content:

## Box
Boxs are data-types that store values. No restriction is placed on how they store these values, though there may be restrictions on some methods if a Box is also an instance of a sub-class of Box.
```python
from monetPy.box import Box
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
from monetPy.semigroups import All

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
from monetPy.semigroups import Sum

Sum(42).concat(Sum(1))  # Sum<43>
Sum(42).concat(Sum(1)).concat(Sum(1))  # Sum<44>
Sum(42).concat(Sum(1).concat(Sum(1)))  # Sum<44>

Sum(42).fold(lambda value: value)  # 42
```

#### First
```python
from monetPy.semigroups import First

First('first').concat(First('Second'))  # First<"first">
First('first').fold(lambda value: value[::-1])  # "tsrif"
```

#### Map
```python
from monetPy.semigroups import Sum, All, First, Map
ingredient1 = Map({'score': Sum(1), 'won': All(True), 'captain': First('captain america')})
ingredient2 = Map({'score': Sum(2), 'won': All(True), 'captain': First('iron man')})
ingredient1.concat(ingredient2)  # Map<{'score': Sum(3), 'won': All(True), 'captain': First('captain america')}>
```

## LazyBox
LazyBox are data-types that store functions. Stored function will not be called until call of fold method
```python
from monetPy.lazy_box import LazyBox

def fn():
    print('fn call')
    return 42
    
def mapper(value):
    print('mapper side effect of ' + value)
    return value + 1
    
def side_effect(value):
    print('side effect of ' + value)
    
lazy_box = LazyBox(fn)
mapped_lazy_box = lazy_box.map(mapper)
mapped_lazy_box.fold(side_effect)  
# fn call
# mapper side effect of 42
# side effect of 42 
```


## Task
Task are data-type for handle execution of functions (in lazy way) transform results of this function and handle errors.
```python
from monetPy.task import Task

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