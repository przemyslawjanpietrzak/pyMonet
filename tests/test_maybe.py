from testers.monad_law_tester import MonadLawTester
from testers.functor_law_tester import FunctorLawTester
from testers.monad_transform_tester import MonadTransformTester
from testers.applicative_law_tester import ApplicativeLawTester

from pymonet.maybe import Maybe
from pymonet.box import Box
from pymonet.either import Left
from pymonet.monad_try import Try
from pymonet.validation import Validation
from pymonet.utils import increase

from hypothesis import given
from hypothesis.strategies import integers

import pytest


class MaybeSpy:

    def mapper(self, value):
        return value + 1

    def binder(self, value):
        return Maybe.just(value + 1)


@pytest.fixture()
def maybe_spy(mocker):
    spy = MaybeSpy()
    mocker.spy(spy, 'mapper')
    mocker.spy(spy, 'binder')

    return spy


@given(integers())
def test_maybe_eq_operator_should_compare_values(integer):

    assert Maybe.just(integer) == Maybe.just(integer)
    assert Maybe.just(None) == Maybe.just(None)

    assert Maybe.just(integer) != Maybe.nothing()


@given(integers())
def test_maybe_map_operator_should_be_applied_only_on_just_value(integer):
    assert Maybe.just(42).map(increase) == Maybe.just(43)
    assert Maybe.nothing().map(increase) == Maybe.nothing()


def test_maybe_map_should_not_call_mapper_when_monad_has_nothing(maybe_spy):
    Maybe.nothing().map(maybe_spy.binder)

    assert maybe_spy.binder.call_count == 0


def test_maybe_bind_should_retrun_result_of_mapper_called_with_maybe_value(maybe_spy):
    assert Maybe.just(42).bind(increase) == 43


def test_maybe_bind_should_not_call_mapper_when_monad_has_nothing(maybe_spy):
    Maybe.nothing().bind(maybe_spy.binder)

    assert maybe_spy.binder.call_count == 0


@given(integers())
def test_maybe_get_or_else_method_should_return_maybe_value_when_monad_is_not_empty(integer):
    assert Maybe.just(integer).get_or_else(0) is integer


@given(integers())
def test_maybe_get_or_else_method_should_return_argument_when_monad_is_empty(integer):
    assert Maybe.nothing().get_or_else(integer) is integer


@given(integers())
def test_maybe_is_nothing_should_return_proper_boolean(integer):
    assert Maybe.just(integer).is_nothing is False
    assert Maybe.nothing().is_nothing is True


def test_maybe_if_filter_returns_false_method_should_return_empty_maybe():
    assert Maybe.just(41).filter(lambda value: value % 2 == 0) == Maybe.nothing()


def test_maybe_if_filter_returns_true_method_should_return_self():
    assert Maybe.just(42).filter(lambda value: value % 2 == 0) == Maybe.just(42)


@given(integers())
def test_maybe_monad_law(integer):
    MonadLawTester(
        monad=Maybe.just,
        value=integer,
        mapper1=lambda value: Maybe.just(value + 1),
        mapper2=lambda value: Maybe.just(value + 2)
    ).test()


@given(integers())
def test_maybe_functor_law(integer):
    FunctorLawTester(
        functor=Maybe.just(integer),
        mapper1=lambda value: value + 1,
        mapper2=lambda value: value + 2
    ).test()


@given(integers())
def test_maybe_transform(integer):
    MonadTransformTester(monad=Maybe.just, value=integer).test(run_to_maybe_test=False)

    assert Maybe.nothing().to_box() == Box(None)
    assert Maybe.nothing().to_either() == Left(None)
    assert Maybe.nothing().to_lazy().get() is None
    assert Maybe.nothing().to_try() == Try(None, is_success=False)
    assert Maybe.nothing().to_validation() == Validation.success(None)


@given(integers())
def test_maybe_applicative_law(integer):
    ApplicativeLawTester(
        applicative=Maybe.just,
        value=integer,
        mapper1=lambda value: value + 1,
        mapper2=lambda value: value + 2,
    ).test()


def test_maybe_ap_on_empty_maybe_should_not_be_applied():
    def lambda_fn():
        raise TypeError
    assert Maybe.nothing().ap(Maybe.just(lambda_fn)) == Maybe.nothing()
    assert Maybe.just(42).ap(Maybe.nothing()) == Maybe.nothing()
