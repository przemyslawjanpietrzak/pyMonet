from testers.monad_law_tester import MonadLawTester
from testers.functor_law_tester import FunctorLawTester
from testers.monad_transform_tester import MonadTransformTester

from pymonet.validation import Validation
from pymonet.either import Left
from pymonet.maybe import Maybe
from pymonet.utils import increase

from hypothesis import given
from hypothesis.strategies import integers

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


@given(integers())
def test_validation_monad_law(integer):
    MonadLawTester(
        monad=Validation.success,
        value=integer,
        mapper1=lambda value: Validation.success(value + 1),
        mapper2=lambda value: Validation.success(value + 2)
    ).test()


@given(integers())
def test_validation_functor_law(integer):
    FunctorLawTester(
        functor=Validation.success(integer),
        mapper1=lambda value: value + 1,
        mapper2=lambda value: value + 2
    ).test()


@given(integers())
def test_validation_transform(integer):
    MonadTransformTester(monad=Validation.success, value=integer).test(run_to_validation_test=False)

    Validation.fail([integer]).to_maybe() == Maybe.nothing()
    Validation.fail([integer]).to_either() == Left([integers])
