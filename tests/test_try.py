from pymonet.monad_try import Try
from pymonet.utils import increase

from hypothesis import given
from hypothesis.strategies import integers

import pytest


def divide(dividend, divisor):
    return dividend / divisor


class TrySpy:

    def fn(self):
        return 42

    def fail(self):
        return 42 / 0

    def binder(self, value):
        return Try.of(divide, value, 2)

    def success_callback(self, value):
        pass

    def fail_callback(self, value):
        pass


@pytest.fixture()
def try_spy(mocker):
    spy = TrySpy()
    mocker.spy(spy, 'fn')
    mocker.spy(spy, 'success_callback')
    mocker.spy(spy, 'fail')
    mocker.spy(spy, 'fail_callback')
    mocker.spy(spy, 'binder')

    return spy


def test_try_should_call_success_callback_with_result_of_function_when_exception_was_not_thrown(try_spy):

    (Try.of(try_spy.fn)
        .on_success(try_spy.success_callback)
        .on_fail(try_spy.fail_callback))

    assert try_spy.fail_callback.call_count == 0
    assert try_spy.success_callback.call_count == 1

    try_spy.success_callback.assert_called_once_with(42)

def test_try_should_call_fail_callback_with_result_of_function_when_exception_was_thrown(try_spy):

    (Try.of(try_spy.fail)
        .on_success(try_spy.success_callback)
        .on_fail(try_spy.fail_callback))

    assert try_spy.fail_callback.call_count == 1
    assert try_spy.success_callback.call_count == 0

def test_try_eq_should_compare_value_and_result_of_try(try_spy):
    assert Try.of(try_spy.fn) == Try.of(try_spy.fn)
    assert Try.of(try_spy.fail) != Try.of(try_spy.fail)

def test_try_should_appied_map_when_exception_was_thrown(try_spy):
    (Try.of(try_spy.fn)
        .map(increase)
        .on_success(try_spy.success_callback)
        .on_fail(try_spy.fail_callback))

    assert try_spy.fail_callback.call_count == 0
    assert try_spy.success_callback.call_count == 1

    try_spy.success_callback.assert_called_once_with(43)

def test_try_should_appied_bind_when_exception_not_was_thrown(try_spy):
    (Try.of(try_spy.fn)
        .bind(lambda value: Try.of(divide, value, 2))
        .on_success(try_spy.success_callback)
        .on_fail(try_spy.fail_callback))

    assert try_spy.fail_callback.call_count == 0
    assert try_spy.success_callback.call_count == 1

    try_spy.success_callback.assert_called_once_with(21)

def test_try_should_not_appied_bind_when_exception_was_thrown(try_spy):
    (Try.of(try_spy.fail)
        .bind(lambda value: Try.of(divide, value, 2))
        .on_success(try_spy.success_callback)
        .on_fail(try_spy.fail_callback))

    assert try_spy.fail_callback.call_count == 1
    assert try_spy.success_callback.call_count == 0

    try_spy.fail_callback.assert_called_once_with(ZeroDivisionError('division by zero',))

def test_when_bind_is_rejected_monad_also_should_be_rejected():

    def success_callback(_):
        assert True is False

    def fail_callback(error):
        assert isinstance(error, ZeroDivisionError)
        assert str(error) == 'float division by zero'

    (Try.of(divide, 42, 2)
        .bind(lambda value: Try.of(divide, value, 0))
        .on_success(success_callback)
        .on_fail(fail_callback))


def test_try_should_not_applied_map_when_exception_thrown():

    def success_callback(_):
        assert True is False

    def fail_callback(error):
        assert isinstance(error, ZeroDivisionError)
        assert str(error) == 'division by zero'

    def mapper(_):
        assert True is False

    (Try.of(divide, 42, 0)
        .map(mapper)
        .on_success(success_callback)
        .on_fail(fail_callback))


def test_get_or_default_method_should_return_value_when_exception_was_not_thrown():
    assert Try.of(divide, 42, 2).get_or_else('Holy Grail') == 21


def test_get_or_default_method_should_return_default_value_when_exception_was_thrown():
    assert Try.of(divide, 42, 0).get_or_else('Holy Grail') == 'Holy Grail'


def test_get_method_should_return_value_with_or_without_exception_thrown():
    assert Try.of(divide, 42, 2).get() == 21

    failed_value = Try.of(divide, 42, 0).get()
    assert isinstance(failed_value, ZeroDivisionError)
    assert str(failed_value) == 'division by zero'


def test_filer_should_converts_to_fail_when_predicate_returns_false():
    filtered = Try.of(divide, 42, 2).filter(lambda value: value % 2 == 0.0)
    assert not filtered.is_success

    not_filtered = Try.of(divide, 42, 2).filter(lambda value: value % 3 == 0.0)
    assert not_filtered.is_success
