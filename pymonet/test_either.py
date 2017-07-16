from pymonet.either import Left, Right
from pymonet.utils import increase


class EitherSpy:

    def error_handler(value, *args):
        pass

    def success_handler(value, *args):
        pass


def test_either_eq_operator_should_compare_values():

    assert Right(42) == Right(42)
    assert Right(42) != Right(43)

    assert Left(42) == Left(42)
    assert Left(42) != Left(43)

    assert Right(42) != Left(42)


def test_mapper_should_be_applied_only_on_current_value():

    assert Left(42).map(increase) == Left(42)
    assert Right(42).map(increase) == Right(43)


def test_is_right_should_return_suitable_value():

    assert Right(42).is_right()
    assert not Left(42).is_right()


def test_is_left_should_return_suitable_value():
    assert Left(42).is_left()
    assert not Right(42).is_left()


def test_fold_should_be_applied_only_on_current_value_and_return_value():

    assert Left(42).fold(increase) == 42
    assert Right(42).fold(increase) == 43


def test_case_method_should_call_proper_handler(mocker):
    either_spy = EitherSpy()
    mocker.spy(either_spy, 'error_handler')
    mocker.spy(either_spy, 'success_handler')

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
