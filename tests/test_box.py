from testers.monad_law_tester import MonadLawTester
from testers.functor_law_tester import FunctorLawTester
from testers.monad_transform_tester import MonadTransformTester
from testers.applicative_law_tester import ApplicativeLawTester

from pymonet.box import Box
from pymonet.utils import increase

from hypothesis import given
from hypothesis.strategies import integers


def test_eq_should_compare_only_box_value():
    assert Box(42) == Box(42)
    assert Box(43) != Box(42)
    assert Box([]) == Box([])
    assert Box({}) == Box({})
    assert Box(None) == Box(None)


def test_map_should_return_box_with_mapped_value():
    box = Box(42)
    assert box.map(increase) == Box(43)


def test_map_should_return_new_instance_of_box():
    box = Box(42)
    mapped_box = box.map(increase)
    assert box is not mapped_box


def test_fold_should_return_result_of_fold_function_called_with_box_value():
    box = Box(42)
    assert box.bind(increase) == 43


@given(integers())
def test_box_monad_law(integer):
    MonadLawTester(
        monad=Box,
        value=integer,
        mapper1=lambda value: Box(value + 1),
        mapper2=lambda value: Box(value + 2)
    ).test()


@given(integers())
def test_box_functor_law(integer):
    FunctorLawTester(
        functor=Box(integer),
        mapper1=lambda value: value + 1,
        mapper2=lambda value: value + 2
    ).test()


@given(integers())
def test_box_transform_monad(integer):
    MonadTransformTester(
        monad=Box,
        value=integer
    ).test(run_to_box_test=False)


@given(integers())
def test_box_applicative_law(integer):
    ApplicativeLawTester(
        applicative=Box,
        value=integer,
        mapper1=lambda value: value + 1,
        mapper2=lambda value: value + 2,
    ).test()
