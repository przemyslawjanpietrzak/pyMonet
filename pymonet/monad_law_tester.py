def _get_monadic_value(monad, monad_value, use_constructor=True):
    return monad(monad_value)


def get_associativity_test(monadic_value, mapper1, mapper2):
    def result():
        value1 = (monadic_value
                  .bind(mapper1)).bind(mapper2)
        value2 = (monadic_value
                  .bind(mapper2)
                  .bind(mapper1))

        assert value1 == value2

    return result


def get_left_unit_test(monad, monad_value, mapper):
    def result():
        monadic_value = _get_monadic_value(monad, monad_value)
        assert monadic_value.bind(mapper) == mapper(monad_value)

    return result


def get_right_unit_data(monad, monad_value, use_constructor=True):
    def result():
        monadic_value = _get_monadic_value(monad, monad_value, use_constructor)
        monadic_value.bind(lambda value: _get_monadic_value(monad, value, use_constructor)) == monadic_value

    return result
