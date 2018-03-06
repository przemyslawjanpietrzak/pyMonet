from pymonet.utils import cond

import pytest


mocked_args = [42]


class CondSpy:

    def cond_function(self, *args):
        assert args == (mocked_args, )
        return True

    def cond_function_false(self, *args):
        assert args == (mocked_args, )
        return False

    def execute_function(self, *args):
        print(args)
        assert args == (mocked_args, )
        return 42

    def execute_function1(self, *args):
        assert args == (mocked_args, )
        return 0


@pytest.fixture
def cond_spy(mocker):
    cond_spy = CondSpy()
    mocker.spy(cond_spy, 'cond_function')
    mocker.spy(cond_spy, 'cond_function_false')
    mocker.spy(cond_spy, 'execute_function')
    mocker.spy(cond_spy, 'execute_function1')

    return cond_spy


def test_cond_should_return_function_with_calls_first_passed_function(cond_spy):
    assert cond([
        (cond_spy.cond_function_false, cond_spy.execute_function1),
        (cond_spy.cond_function, cond_spy.execute_function)
    ])(mocked_args)

    assert cond_spy.cond_function_false.call_count == 1
    assert cond_spy.cond_function.call_count == 1
    assert cond_spy.execute_function1.call_count == 0
    assert cond_spy.execute_function.call_count == 1
