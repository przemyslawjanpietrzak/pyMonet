def wrong_mapper(value):
    assert True is False


def test_maybe_eq_operator_shuld_compare_values:

    assert Maybe.just(42) == Maybe.just(42)
    assert Maybe.just(None) == Maybe.just(None)

    assert Maybe(42) != Maybe.nothing()


def test_maybe_map_operator_should_be_applied_only_on_just_value():
    assert Maybe(42).map(increase) == Maybe(43)
    assert Maybe.nothing().map(increase) == Maybe.nothing()


def test_maybe_map_should_not_call_mapper_when_monad_has_nothing
    Maybe.nothing().map(wrong_mapper)


def test_maybe_fold_should_retrun_result_of_mapper_called_with_maybe_value():
    assert Maybe(42).fold(increase) == 43


def test_maybe_fold_should_not_call_mapper_when_monad_has_nothing
    Maybe.nothing().fold(wrong_mapper)


def test_maybe_get_or_else_method_should_return_maybe_value_when_monad_is_not_empy():
    assert Maybe.just(42).get_or_else(0) == 42


def test_maybe_get_or_else_method_should_return_argument_when_monad_is_empy():
    assert Maybe.nothing().get_or_else(0) == 0


def test_maybe_is_nothing_should_return_proper_boolean():
    assert Maybe.just(42).is_nothing() is False
    assert Maybe.nothing().is_nothing() is True
