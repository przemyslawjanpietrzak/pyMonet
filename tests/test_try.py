from testers.functor_law_tester import FunctorLawTester
from testers.monad_law_tester import MonadLawTester

from pymonet.monad_try import Try
from pymonet.utils import increase

from hypothesis import given
from hypothesis.strategies import text, integers

import pytest


def divide(dividend, divisor):
    return dividend / divisor


class TrySpy:

    def fn(self):
        return 42

    def fail(self):
        return 42 / 0

    def mapper(self, value):
        return value + 1

    def binder(self, value):
        return Try.of(divide, value, 2)

    def fail_binder(self, value):
        return Try.of(divide, value, 0)

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
    mocker.spy(spy, 'fail_binder')
    mocker.spy(spy, 'mapper')

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
        .bind(try_spy.binder)
        .on_success(try_spy.success_callback)
        .on_fail(try_spy.fail_callback))

    assert try_spy.fail_callback.call_count == 0
    assert try_spy.success_callback.call_count == 1
    assert try_spy.binder.call_count == 1

    try_spy.success_callback.assert_called_once_with(21)
    try_spy.binder.assert_called_once_with(42)


def test_try_should_not_appied_bind_when_exception_was_thrown(try_spy):
    (Try.of(try_spy.fail)
        .bind(try_spy.binder)
        .on_success(try_spy.success_callback)
        .on_fail(try_spy.fail_callback))

    assert try_spy.fail_callback.call_count == 1
    assert try_spy.binder.call_count == 0
    assert try_spy.success_callback.call_count == 0


def test_when_bind_is_rejected_monad_also_should_be_rejected(try_spy):
    (Try.of(try_spy.fn)
        .bind(try_spy.fail_binder)
        .on_success(try_spy.success_callback)
        .on_fail(try_spy.fail_callback))

    assert try_spy.fail_callback.call_count == 1
    assert try_spy.fail_binder.call_count == 1
    assert try_spy.success_callback.call_count == 0


def test_try_should_not_applied_map_when_exception_thrown(try_spy):
    (Try.of(try_spy.fail)
        .map(try_spy.mapper)
        .on_success(try_spy.success_callback)
        .on_fail(try_spy.fail_callback))

    assert try_spy.fail_callback.call_count == 1
    assert try_spy.fail_binder.call_count == 0
    assert try_spy.mapper.call_count == 0


@given(text())
def test_get_or_default_method_should_return_value_when_exception_was_not_thrown(try_spy, text):
    assert Try.of(try_spy.fn).get_or_else(text) == 42


def test_get_or_default_method_should_return_default_value_when_exception_was_thrown(try_spy):
    assert Try.of(try_spy.fail).get_or_else(text) is text


def test_filer_should_converts_to_fail_when_predicate_returns_false(try_spy):
    filtered = Try.of(try_spy.fn).filter(lambda value: value % 4 == 0.0)
    assert not filtered.is_success

    not_filtered = Try.of(try_spy.fn).filter(lambda value: value % 3 == 0.0)
    assert not_filtered.is_success


@given(integers())
def test_try_functor_laws(integer):
    FunctorLawTester(
        functor=Try.of(integer),
        mapper1=lambda value: value + 1,
        mapper2=lambda value: value + 1,
    ).test()


@given(integers())
def test_try_monad_associativity_law(integer):
    MonadLawTester(
        monad=Try.of,
        value=lambda: integer,
        mapper1=lambda value: Try.of(lambda: value + 1),
        mapper2=lambda value: Try.of(lambda: value + 2),
    ).test(run_left_law_test=False, run_right_law_test=False)


@given(integers())
def test_try_monad_left_unit_law(integer):
    assert Try(integer, True).bind(lambda value: Try(value + 1, True)) == Try(increase(integer), True)


@given(integers())
def test_try_monad_right_unit_law(integer):
    assert Try(integer, True).bind(lambda value: Try(value, True)) == Try(integer, True)
