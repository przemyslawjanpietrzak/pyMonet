import pytest
from pymonet.box import Box


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
    assert box.fold(lambda value: value + 1) == 43
