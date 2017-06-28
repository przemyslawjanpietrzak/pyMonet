import pytest
from pymonet.lazy_box import LazyBox
from pymonet.utils import identity


class LazyBoxSpy:

    def fn(self):
        return 42

    def side_effect(self, input):
        return input


def test_lazy_box(mocker):
    """
    input function and all map functions should be called during called fold method
    """

    lazy_box_spy = LazyBoxSpy()
    mocker.spy(lazy_box_spy, 'fn')
    mocker.spy(lazy_box_spy, 'side_effect')

    lazy_box = LazyBox(lazy_box_spy.fn)
    assert lazy_box_spy.fn.call_count == 0

    lazy_box = lazy_box.map(lazy_box_spy.side_effect)
    assert lazy_box_spy.fn.call_count == 0
    assert lazy_box_spy.side_effect.call_count == 0

    lazy_box = lazy_box.map(lambda number: number + 1)
    assert lazy_box_spy.fn.call_count == 0
    assert lazy_box_spy.side_effect.call_count == 0

    assert lazy_box.fold(lambda number: number + 1) == 44
    assert lazy_box_spy.fn.call_count == 1
    assert lazy_box_spy.side_effect.call_count == 1

