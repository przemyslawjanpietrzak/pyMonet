from testers.monad_law_tester import MonadLawTester
from testers.functor_law_tester import FunctorLawTester
from testers.monad_transform_tester import MonadTransformTester
from testers.applicative_law_tester import ApplicativeLawTester

from pymonet.either import Left, Right
from pymonet.utils import increase

from hypothesis import given
from hypothesis.strategies import integers

import pytest


class EitherSpy:

    def error_handler(value, *args):
        pass

    def success_handler(value, *args):
        pass


@pytest.fixture()
def either_spy(mocker):
    spy = EitherSpy()
    mocker.spy(spy, 'error_handler')
    mocker.spy(spy, 'success_handler')

    return spy


@given(integers())
def test_either_eq_operator_should_compare_values(integer):

    assert Right(integer) == Right(integer)
    assert Right(integer) != Right(integer + 1)

    assert Left(integer) == Left(integer)
    assert Left(integer) != Left(integer + 1)

    assert Right(integer) != Left(integer)


@given(integers())
def test_mapper_should_be_applied_only_on_current_value(integer):

    assert Left(integer).map(increase) == Left(integer)
    assert Right(integer).map(increase) == Right(increase(integer))


@given(integers())
def test_is_right_should_return_suitable_value(integer):
    assert Right(integer).is_right()
    assert not Left(integer).is_right()


@given(integers())
def test_is_left_should_return_suitable_value(integer):
    assert Left(integer).is_left()
    assert not Right(integer).is_left()


def test_bind_should_be_applied_only_on_current_value_and_return_value():
    assert Left(42).bind(lambda value: Right(value + 1)).value == 42
    assert Right(42).bind(lambda value: Right(value + 1)).value == 43
    assert Right(42).bind(lambda value: Left(value + 1)).value == 43


def test_case_method_should_call_proper_handler(either_spy):
    Left(42).case(
        success=either_spy.success_handler,
        error=either_spy.error_handler
    )

    assert either_spy.error_handler.call_count == 1
    assert either_spy.success_handler.call_count == 0

    Right(42).case(
        success=either_spy.success_handler,
        error=either_spy.error_handler
    )

    assert either_spy.error_handler.call_count == 1
    assert either_spy.success_handler.call_count == 1


@given(integers())
def test_either_monad_law(integer):
    MonadLawTester(
        monad=Right,
        value=integer,
        mapper1=lambda value: Right(value + 1),
        mapper2=lambda value: Right(value + 2),
    ).test()

    MonadLawTester(
        monad=Left,
        value=integer,
        mapper1=lambda value: Left(value + 1),
        mapper2=lambda value: Left(value + 2),
    ).test(run_left_law_test=False)


@given(integers())
def test_either_functor_law(integer):
    FunctorLawTester(
        functor=Right(integer),
        mapper1=lambda value: value + 1,
        mapper2=lambda value: value + 2,
    ).test()

    FunctorLawTester(
        functor=Left(integer),
        mapper1=lambda value: value + 1,
        mapper2=lambda value: value + 2,
    ).test()


@given(integers())
def test_either_transform(integer):
    MonadTransformTester(monad=Right, value=integer).test(run_to_either_test=False)
    MonadTransformTester(monad=Left, value=integer, is_fail=True).test(run_to_either_test=False)


@given(integers())
def test_either_applicative_law(integer):
    ApplicativeLawTester(
        applicative=Right,
        value=integer,
        mapper1=lambda value: value + 1,
        mapper2=lambda value: value + 2
    ).test()


@given(integers())
def test_either_ap_on_left_should_not_be_applied(integer):
    def lambda_fn():
        raise TypeError
    assert Left(integer).ap(Right(lambda_fn)) == Left(integer)
    assert Left(integer).ap(Left(lambda_fn)) == Left(integer)
