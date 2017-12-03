from pymonet.utils import memoize


result = {'key': 'value'}


class MemoizeSpy:

    def fn(*args):
        return args

    def key(_, value, new_value):
        return value['compare_key'] == new_value['compare_key']


def test_utils_memoize_should_call_fn_once_when_args_are_equal(mocker):
    memoize_spy = MemoizeSpy()
    mocker.spy(memoize_spy, 'fn')

    momoized_function = memoize(memoize_spy.fn)
    result1 = momoized_function(42)

    assert memoize_spy.fn.call_count == 1

    result2 = momoized_function(42)
    assert memoize_spy.fn.call_count == 1
    assert result1 is result2


def test_utils_memoize_should_call_fn_when_arguments_change(mocker):
    memoize_spy = MemoizeSpy()
    mocker.spy(memoize_spy, 'fn')

    momoized_function = memoize(memoize_spy.fn)
    result1 = momoized_function(42)

    assert memoize_spy.fn.call_count == 1

    result2 = momoized_function(43)

    assert memoize_spy.fn.call_count == 2
    assert result1 is not result2


def test_utils_memoize_should_cache_output_when_key_returns_truthy(mocker):
    memoize_spy = MemoizeSpy()
    mocker.spy(memoize_spy, 'fn')
    mocker.spy(memoize_spy, 'key')

    momoized_function = memoize(memoize_spy.fn, memoize_spy.key)
    result1 = momoized_function({'compare_key': 42, 'other_key': 0})
    result2 = momoized_function({'compare_key': 42, 'other_key': 1})

    assert result1 is result2
    assert memoize_spy.fn.call_count == 1

    result3 = momoized_function({'compare_key': 41, 'other_key': 1})

    assert result3 is not result1
    assert memoize_spy.fn.call_count == 2
