from pymonet.box import Box
from pymonet.monad_law_tester import get_associativity_test, get_left_unit_test, get_right_unit_data


def test_eq_should_compare_only_box_value():
    assert Box(42) == Box(42)
    assert Box(43) != Box(42)
    assert Box([]) == Box([])
    assert Box({}) == Box({})
    assert Box(None) == Box(None)


def test_map_should_return_box_with_mapped_value():
    box = Box(42)
    assert box.map(lambda value: value + 1) == Box(43)


def test_map_should_return_new_instance_of_box():
    box = Box(42)
    mapped_box = box.map(lambda value: value + 1)
    assert box is not mapped_box


def test_fold_should_return_result_of_fold_function_called_with_box_value():
    box = Box(42)
    assert box.bind(lambda value: value + 1) == 43


def test_ap_should_return_result_of_function_in_box():

    box = Box(42)
    assert (box.ap(
        Box(lambda value: value + 1)
    )) == Box(43)


def test_maybe_associativity_law():
    get_associativity_test(
        monadic_value=Box(42),
        mapper1=lambda value: Box(value + 1),
        mapper2=lambda value: Box(value + 2)
    )()


def test_maybe_left_unit_law():
    get_left_unit_test(Box, 42, lambda value: Box(value + 1))()


def test_maybe_right_unit_data_law():
    get_right_unit_data(Box, 42)()
