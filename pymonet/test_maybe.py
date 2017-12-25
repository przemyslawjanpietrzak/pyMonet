from pymonet.maybe import Maybe
from pymonet.box import Box
from pymonet.either import Left
from pymonet.monad_try import Try
from pymonet.utils import increase, identity
from pymonet.monad_law_tester import MonadLawTester
from pymonet.functor_law_tester import FunctorLawTester
from pymonet.transform_monad_tester import TransformMonadTester

from hypothesis import given
from hypothesis.strategies import integers


def wrong_mapper(_):
    assert True is False


def test_maybe_eq_operator_shuld_compare_values():

    assert Maybe.just(42) == Maybe.just(42)
    assert Maybe.just(None) == Maybe.just(None)

    assert Maybe.just(42) != Maybe.nothing()


def test_maybe_map_operator_should_be_applied_only_on_just_value():
    assert Maybe.just(42).map(increase) == Maybe.just(43)
    assert Maybe.nothing().map(increase) == Maybe.nothing()


def test_maybe_map_should_not_call_mapper_when_monad_has_nothing():
    Maybe.nothing().map(wrong_mapper)


def test_maybe_bind_should_retrun_result_of_mapper_called_with_maybe_value():
    assert Maybe.just(42).bind(increase) == 43


def test_maybe_bind_should_not_call_mapper_when_monad_has_nothing():
    Maybe.nothing().bind(wrong_mapper)


def test_maybe_get_or_else_method_should_return_maybe_value_when_monad_is_not_empy():
    assert Maybe.just(42).get_or_else(0) == 42


def test_maybe_get_or_else_method_should_return_argument_when_monad_is_emtpy():
    assert Maybe.nothing().get_or_else(0) == 0


def test_maybe_is_nothing_should_return_proper_boolean():
    assert Maybe.just(42).is_nothing is False
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
    TransformMonadTester(monad=Maybe.just, value=integer).test(run_to_maybe_test=False)

    assert Maybe.nothing().to_box() == Box(None)
    assert Maybe.nothing().to_either() == Left(None)
    assert Maybe.nothing().to_lazy().fold(identity) is None
    assert Maybe.nothing().to_try() == Try(None, is_success=False)
