from tests.applicative_law_tester import  ApplicativeLawTester
from tests.functor_law_tester import FunctorLawTester

from pymonet.lazy import Lazy
from pymonet.validation import Validation
from pymonet.utils import identity, increase

from hypothesis import given
from hypothesis.strategies import integers


from random import random


class LazySpy:

    def mapper(self, input):
        return input + 1

    def fn(self):
        return 42

    def binder(self, value):
        return Lazy(value + 1)


def fn():
    return 42


def fn1():
    return 43


def test_applicative_should_call_stored_function_during_fold_method_call(mocker):

    lazy_spy = LazySpy()
    mocker.spy(lazy_spy, 'fn')

    applicative = Lazy(lazy_spy.fn)

    assert lazy_spy.fn.call_count == 0

    assert applicative.get() == 42
    assert lazy_spy.fn.call_count == 1


def test_applicative_should_not_call_mapper_until_call_get(mocker):

    lazy_spy = LazySpy()
    mocker.spy(lazy_spy, 'fn')
    mocker.spy(lazy_spy, 'mapper')
    mocker.spy(lazy_spy, 'binder')

    applicative = Lazy(lazy_spy.fn).map(lazy_spy.mapper)

    assert lazy_spy.fn.call_count == 0
    assert lazy_spy.mapper.call_count == 0

    # applicative = applicative.bind(lazy_spy.binder)
    # assert lazy_spy.fn.call_count == 0
    # assert lazy_spy.mapper.call_count == 0
    # assert lazy_spy.binder.call_count == 0

    assert applicative.get() == 43
    assert lazy_spy.fn.call_count == 1
    assert lazy_spy.mapper.call_count == 1


def test_applicative_should_not_call_binder_until_call_get(mocker):

    lazy_spy = LazySpy()
    mocker.spy(lazy_spy, 'fn')
    mocker.spy(lazy_spy, 'binder')

    lazy = Lazy(lazy_spy.fn)
    assert lazy_spy.fn.call_count == 0
    assert lazy_spy.binder.call_count == 0

    lazy = lazy.bind(lazy_spy.binder)
    assert lazy_spy.fn.call_count == 0
    assert lazy_spy.binder.call_count == 0

    result = lazy.get()
    assert lazy_spy.fn.call_count == 1
    assert lazy_spy.binder.call_count == 1
    assert result == 43


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


@given(integers())
def test_transform_to_validation_should_validation(integer):
    assert Lazy(lambda: integer).to_validation() == Validation.success(integer)


@given(integers())
def test_lazy_applicative(integer):
    assert Lazy(identity).ap(Lazy(lambda: integer)).get() == Lazy(lambda: integer).get()
    assert Lazy(increase).ap(Lazy(lambda: integer)).get() == increase(integer)



@given(integers())
def test_lazy_functor_law(integer):
    FunctorLawTester(
        functor=Lazy(lambda: integer),
        mapper1=lambda value: value + 1,
        mapper2=lambda value: value + 2,
        get_fn=lambda lazy: lazy.get()
    ).test()