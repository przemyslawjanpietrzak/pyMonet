from pymonet.validation import Validation
from pymonet.maybe import Maybe
from pymonet.either import Left, Right
from pymonet.monad_try import Try
from pymonet.box import Box
from pymonet.utils import increase, identity
from pymonet.monad_law_tester import get_associativity_test, get_left_unit_test, get_right_unit_data

from hypothesis import given
from hypothesis.strategies import text

import re


def test_validation_map():
    assert Validation.success(42).map(increase) == Validation.success(43)


def test_validation_bind():
    assert (Validation
            .success(42)
            .bind(lambda value: Validation.success(value + 1))) == Validation.success(43)


def test_validation_is_success():
    assert Validation.success().is_success()


def test_validation_is_fail():
    assert Validation.fail(['fail']).is_fail()


def validate_length(value):
    if len(value) < 5:
        return Validation.fail(['value not long enough'])
    return Validation.success()


def validate_uppercase(value):
    if value[0].upper() != value[0]:
        return Validation.fail(['value not uppercase'])
    return Validation.success()


def validate_contains_special_character(value):
    if re.match(r'^[a-zA-Z0-9_]*$', value):
        return Validation.fail(['value not contains special character'])
    return Validation.success()


def validate(value):
    return (Validation.success(value)
            .ap(validate_length)
            .ap(validate_uppercase)
            .ap(validate_contains_special_character))


def test_validation_applicative():
    assert validate('Success$') == Validation.success('Success$')

    assert validate('Success') == Validation(value='Success', errors=['value not contains special character'])

    assert validate('success$') == Validation(value='success$', errors=['value not uppercase'])
    assert validate('S$') == Validation(value='S$', errors=['value not long enough'])

    assert validate('success') == Validation(value='success', errors=[
        'value not uppercase',
        'value not contains special character'
    ])
    assert validate('s$') == Validation(value='s$', errors=[
        'value not long enough',
        'value not uppercase'
    ])
    assert validate('success') == Validation(value='success', errors=[
        'value not uppercase',
        'value not contains special character'
    ])

    assert validate('s') == Validation(value='s', errors=[
        'value not long enough',
        'value not uppercase',
        'value not contains special character'
    ])


def test_Validation_associativity_law():
    get_associativity_test(
        monadic_value=Validation.success(42),
        mapper1=lambda value: Validation.success(value + 1),
        mapper2=lambda value: Validation.success(value + 2)
    )()


def test_Validation_left_unit_law():
    get_left_unit_test(Validation.success, 42, lambda value: Validation.success(value + 1))
    get_left_unit_test(Validation.fail, [42], lambda value: Validation.success(value + 1))


def test_Validation_right_unit_data_law():
    get_right_unit_data(Validation.success, 42)
    get_right_unit_data(Validation.fail, [42])


@given(text())
def test_transform_to_box_should_return_box(integer):
    assert Validation.success(integer).to_box() == Box(integer)
    assert Validation.fail(['fail']).to_box() == Box(None)


@given(text())
def test_transform_to_either_should_return_either(integer):
    assert Validation.success(integer).to_either() == Right(integer)
    assert Validation.fail(['fail']).to_either() == Left(['fail'])


@given(text())
def test_transform_to_maybe_should_return_maybe(integer):
    assert Validation.success(integer).to_maybe() == Maybe.just(integer)
    assert Validation.fail(['fail']).to_maybe() == Maybe.nothing()


@given(text())
def test_transform_to_lazy_should_return_lazy(integer):
    assert Validation.success(integer).to_lazy().fold(identity) == integer
    assert Validation.fail(['fail']).to_lazy().fold(identity) is None


@given(text())
def test_transform_to_try_should_return_try(integer):
    assert Validation.success(integer).to_try() == Try(integer, is_success=True)
    assert Validation.fail(['fail']).to_try() == Try(None, is_success=False)
