from tests.monad_law_tester import MonadLawTester
from tests.functor_law_tester import FunctorLawTester
from tests.monad_transform_tester import MonadTransformTester

from pymonet.reader import Reader

from hypothesis import given
from hypothesis.strategies import integers


class ReaderSpy:

    def fn(self, value):
        return value + 1

    def mapper(self, value):
        return value + 1

    def binder(self, value):
        return Reader.of(value + 1)


@given(integers())
def test_reader_should_call_constructor_fn_during_get_method(mocker, integer):

    reader_spy = ReaderSpy()
    mocker.spy(reader_spy, 'fn')

    reader = Reader(reader_spy.fn)
    assert reader_spy.fn.call_count == 0
    assert reader.get(integer) == integer + 1
    assert reader_spy.fn.call_count == 1


@given(integers())
def test_reader_should_call_mapper_during_get_method(mocker, integer):

    reader_spy = ReaderSpy()
    mocker.spy(reader_spy, 'fn')
    mocker.spy(reader_spy, 'mapper')

    reader = Reader(lambda value: value + 1).map(reader_spy.mapper)
    assert reader_spy.mapper.call_count == 0

    result = reader.get(integer)
    assert result == integer + 2
    assert reader_spy.mapper.call_count == 1


@given(integers())
def test_reader_should_call_binder_during_get_method(mocker, integer):

    reader_spy = ReaderSpy()
    mocker.spy(reader_spy, 'binder')

    reader = Reader(lambda value: value + 1).bind(reader_spy.binder)
    assert reader_spy.binder.call_count == 0

    result = reader.get(integer)
    assert result == integer + 2
    assert reader_spy.binder.call_count == 1

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


# @given(integers())
# def test_reader_transform(integer):
#     MonadTransformTester(monad=Reader.of, value=integer).test(run_to_reader_test=False)


@given(integers())
def test_reader_monad_law(integer):
    MonadLawTester(
        monad=Reader.of,
        value=integer,
        mapper1=lambda value: Reader.of(value + 1),
        mapper2=lambda value: Reader.of(value + 2),
        call_fn=lambda reader: reader.get(integer)
    ).test()


@given(integers())
def test_maybe_functor_law(integer):
    FunctorLawTester(
        functor=Reader.of(integer),
        mapper1=lambda value: value + 1,
        mapper2=lambda value: value + 2,
        call_fn=lambda reader: reader.get(integer)
    ).test()