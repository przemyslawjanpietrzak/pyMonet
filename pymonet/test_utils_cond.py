from pymonet.utils import cond

mocked_args = [42]

class CondSpy:

    def condFunction(*args):
        assert args is mocked_args
        return True

    def condFunctionFalse(*args):
        assert args is mocked_args
        return False

    def executeFunction(*args):
        assert args is mocked_args
        return 42

    def executeFunction1(*args):
        assert args is mocked_args
        return 0


def test_cond_should_return_function_with_calls_first_passed_function(mocker):

    condSpy = CondSpy()
    mocker.spy(condSpy, 'condFunction')
    mocker.spy(condSpy, 'condFunctionFalse')
    mocker.spy(condSpy, 'executeFunction')

    assert cond([
        [condSpy.condFunctionFalse, condSpy.executeFunction1],
        [condSpy.condFunction, condSpy.executeFunction]
    ])(mocked_args) == 42

    assert condSpy.condFunctionFalse.fn.call_count == 1
    assert condSpy.condFunction.fn.call_count == 1
    assert condSpy.executeFunction1.fn.call_count == 0
    assert condSpy.executeFunction.fn.call_count == 1
