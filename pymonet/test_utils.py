from pymonet.utils import \
    identity,\
    increase,\
    compose,\
    eq,\
    pipe,\
    curried_map as map,\
    curried_filter as filter


def test_identity_should_return_first_argument():
    assert identity(42) is 42
    assert identity('string') is 'string'
    assert identity([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert identity(None) is None


def test_compose_should_applied_function_on_value_and_return_it_result():
    assert compose(42, increase) == 43
    assert compose(42, increase, increase) == 44
    assert compose(42, increase, increase, increase) == 45


def test_compose_should_appield_functions_from_last_to_first():
    assert compose(42, increase, lambda value: value * 2) == 85


def test_eq():
    assert eq(42, 42)
    assert eq(42)(42)


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


def test_pipe_should_appield_functions_from_first_to_last():
    assert pipe(42, increase, lambda value: value * 2) == 86
