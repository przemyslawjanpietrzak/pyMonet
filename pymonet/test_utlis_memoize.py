from hypothesis import given
from hypothesis.strategies import text, integers

from pymonet.utils import memoize


result = { 'key': value }

class MemoizeSpy:

    def fn(*args):
        return result

    def key(value, new_value): 
        return value['compare_key'] == new_value['compare_key']


def test_utils_memoize_should_call_fn_once_when_args_are_equal(mocker):
    memoize_spy = MemoizeSpy()
    mocker.spy(memoize_spy, 'fn')  

    assert memoize_spy.fn.call_count == 0

    momoized_function = memoize(memoize_spy.fn)
    result1 = momoized_function(42)

    assert memoize_spy.fn.call_count == 1

    result2 = momoized_function(42)
    assert memoize_spy.fn.call_count == 1
    assert result1 is result2


def test_utils_memoize_should_call_fn_when_arguments_change(mocker):
    memoize_spy = MemoizeSpy()
    mocker.spy(memoize_spy, 'fn')

    assert memoize_spy.fn.call_count == 0

    momoized_function = memoize(memoize_spy.fn)
    result1 = momoized_function(42)

    assert memoize_spy.fn.call_count == 1

    result2 = momoized_function(43)

    assert memoize_spy.fn.call_count == 2


