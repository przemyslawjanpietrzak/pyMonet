from hypothesis import given
from hypothesis.strategies import text, integers, lists

from pymonet.utils import \
    identity,\
    increase,\
    compose,\
    eq,\
    pipe,\
    curried_map as map,\
    curried_filter as filter,\
    find


@given(text(), integers())
def test_identity_should_return_first_argument(text, integer):
    assert identity(text) is text
    assert identity(integer) is integer


@given(integers())
def test_compose_should_applied_function_on_value_and_return_it_result(integer):
    assert compose(integer, increase) == integer + 1
    assert compose(integer, increase, increase) == integer + 2
    assert compose(integer, increase, increase, increase) == integer + 3


@given(integers())
def test_compose_should_appield_functions_from_last_to_first(integer):
    assert compose(integer, increase, lambda value: value * 2) == (integer * 2) + 1


@given(text())
def test_eq(text):
    assert eq(text, text)
    assert eq(text)(text)


def test_compose_with_collections():
    def is_odd(value): return value % 2 == 0

    assert compose(
        list(range(10)),
        map(increase),
        filter(is_odd)
    ) == [1, 3, 5, 7, 9]

    assert compose(
        list(range(10)),
        filter(is_odd),
        map(increase)
    ) == [2, 4, 6, 8, 10]


@given(integers())
def test_pipe_should_appield_functions_from_first_to_last(integer):
    assert pipe(integer, increase, lambda value: value * 2) == (integer + 1) * 2


@given(
    lists(elements=integers(), min_size=1, max_size=1000, unique=True),
    integers()
)
def test_find_should_return_none_when_item_is_not_in_collection_otherwise_should_return_item(lst, integer):
    lst_copy = []
    lst_copy.extend(lst)
    lst_copy.append(integer)

    assert find(lst_copy, eq(integer)) == integer
    assert find(lst[1:], eq(lst[0])) is None
