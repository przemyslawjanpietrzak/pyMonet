from pymonet.lazy import Lazy

from random import random


class LazySpy:

    def mapper(self, input):
        return input + 1

    def fn(self):
        return 42

    def fold_function(self, value):
        return value + 1


def fn():
    return 42


def fn1():
    return 43


def test_applicative_should_call_stored_function_during_fold_method_call(mocker):

    lazy_spy = LazySpy()
    mocker.spy(lazy_spy, 'fn')

    applicative = Lazy(lazy_spy.fn)

    assert lazy_spy.fn.call_count == 0

    assert applicative.fold(lambda number: number + 1) == 43
    assert lazy_spy.fn.call_count == 1


def test_applicative_should_call_mapper_during_fold_method_call(mocker):

    lazy_spy = LazySpy()
    mocker.spy(lazy_spy, 'fn')
    mocker.spy(lazy_spy, 'mapper')
    mocker.spy(lazy_spy, 'fold_function')

    applicative = Lazy(lazy_spy.fn).map(lazy_spy.mapper)

    assert lazy_spy.mapper.call_count == 0

    assert applicative.fold(lazy_spy.fold_function) == 44
    assert lazy_spy.mapper.call_count == 1
    assert lazy_spy.fold_function.call_count == 1


def test_applicative_should_call_memoize_saved_value(mocker):

    lazy_spy = LazySpy()
    mocker.spy(lazy_spy, 'fn')

    lazy = Lazy(lazy_spy.fn)

    value1 = lazy.get()
    assert lazy_spy.fn.call_count == 1

    value2 = lazy.get()
    assert lazy_spy.fn.call_count == 1

    assert value1 is value2


def test_applicative_eq():

    assert Lazy(fn) != {}
    assert Lazy(fn) != []

    assert Lazy(fn) != Lazy(fn1)
    assert Lazy(fn) == Lazy(fn)


def test_applicative_eq_evaluated():

    lazy1 = Lazy(fn)
    lazy2 = Lazy(fn)

    lazy1.get()
    assert lazy1 != lazy2

    lazy2.get()
    assert lazy1 == lazy2


def test_applicative_eq_value():

    lazy1 = Lazy(random)
    lazy2 = Lazy(random)

    lazy1.get()
    lazy2.get()

    assert lazy1 == lazy1
    assert lazy2 == lazy2
    assert lazy1 != lazy2
