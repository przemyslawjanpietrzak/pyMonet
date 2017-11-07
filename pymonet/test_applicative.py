from pymonet.applicative import Applicative


class ApplicativeSpy:

    def mapper(self, input):
        return input + 1

    def fn(self):
        return 42


def test_applicative_should_call_stored_function_during_fold_method_call(mocker):

    applicative_spy = ApplicativeSpy()
    mocker.spy(applicative_spy, 'fn')

    applicative = Applicative(applicative_spy.fn)

    assert applicative_spy.fn.call_count == 0

    assert applicative.fold(lambda number: number + 1) == 43
    assert applicative_spy.fn.call_count == 1


def test_applicative_should_call_mapper_during_fold_method_call(mocker):

    applicative_spy = ApplicativeSpy()
    mocker.spy(applicative_spy, 'fn')
    mocker.spy(applicative_spy, 'mapper')

    applicative = Applicative(applicative_spy.fn).map(applicative_spy.mapper)

    assert applicative_spy.mapper.call_count == 0

    assert applicative.fold(lambda number: number + 1) == 44
    assert applicative_spy.mapper.call_count == 1

