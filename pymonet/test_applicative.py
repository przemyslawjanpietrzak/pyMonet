from pymonet.applicative import Applicative


class ApplicativeSpy:

    def fn(self):
        return 42

    def side_effect(self, input):
        return input


def test_applicative(mocker):
    """
    input function and all map functions should be called during called fold method
    """

    applicative_spy = ApplicativeSpy()
    mocker.spy(applicative_spy, 'fn')
    mocker.spy(applicative_spy, 'side_effect')

    applicative = Applicative(applicative_spy.fn)
    assert applicative_spy.fn.call_count == 0

    applicative = applicative.map(applicative_spy.side_effect)
    assert applicative_spy.fn.call_count == 0
    assert applicative_spy.side_effect.call_count == 0

    applicative = applicative.map(lambda number: number + 1)
    assert applicative_spy.fn.call_count == 0
    assert applicative_spy.side_effect.call_count == 0

    assert applicative.fold(lambda number: number + 1) == 44
    assert applicative_spy.fn.call_count == 1
    assert applicative_spy.side_effect.call_count == 1
