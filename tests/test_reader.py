from pymonet.reader import Reader

from hypothesis import given
from hypothesis.strategies import integers


class ReaderSpy:

    def fn(self, value):
        return value + 1

    def mapper(self, value):
        return value + 1


def test_reader_should_call_constructor_fn_during_get_method(mocker):

    reader_spy = ReaderSpy()
    mocker.spy(reader_spy, 'fn')

    reader = Reader(reader_spy.fn)
    assert reader_spy.call_count == 0
    assert reader.get() == 42
    assert reader_spy.call_count == 1


@given(integers())
def test_reader_should_call_mapper_during_get_method(mocker, integer):

    reader_spy = ReaderSpy()
    mocker.spy(reader_spy, 'fn')
    mocker.spy(reader_spy, 'mapper')

    reader = Reader(lambda value: value + 1).map(reader_spy.mapper)
    assert reader_spy.mapper.call_count == 0
    assert reader_spy.fn.call_count == 0

    result = reader.get(integer)
    assert reader_spy.mapper.call_count == 0
    assert reader_spy.fn.call_count == 0
    assert result == integer + 2


@given(integers())
def test_reader_should_apply_get_arguments_to_constructor_function(integer):
    def constructor_fn_spy(arg):
        assert arg is integer
        return integer

    value = Reader(constructor_fn_spy).get(integer)
    assert value is integer  


@given(integers())
def test_reader_of_should_return_reader_with_function_returning_of_argument(integer):
    assert Reader.of(integer).get() == integer





