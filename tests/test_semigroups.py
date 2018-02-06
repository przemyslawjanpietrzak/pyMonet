from hypothesis import given
from hypothesis.strategies import text, integers, booleans, dictionaries

from testers.semigroup_law_tester import SemigroupLawTester
from testers.monoid_law_tester import MonoidLawTester

from pymonet.semigroups import Sum, All, First, Map
from pymonet.utils import identity


@given(integers(), integers(), integers())
def test_sum(x, y, z):
    SemigroupLawTester(
        semigroup=Sum,
        value1=x,
        value2=y,
        value3=z,
        result=Sum(x + y + z)
    ).test()


@given(integers())
def test_sum_monoid(integer):
    MonoidLawTester(
        monoid=Sum,
        value=integer
    ).test()


@given(booleans(), booleans(), booleans())
def test_all(bool1, bool2, bool3):
    SemigroupLawTester(
        semigroup=All,
        value1=bool1,
        value2=bool2,
        value3=bool3,
        result=All(bool1 and bool2 and bool3)
    ).test()


@given(integers())
def test_all_monoid(integer):
    MonoidLawTester(
        monoid=All,
        value=integer
    ).test()


@given(text(), text(), text())
def test_first(text1, text2, text3):
    SemigroupLawTester(
        semigroup=First,
        value1=text1,
        value2=text2,
        value3=text3,
        result=First(text1)
    ).test()


@given(
    integers(), integers(), integers(),
    booleans(), booleans(), booleans(),
    text(), text(), text()
)
def test_map(integer1, integer2, integer3, boolean1, boolean2, boolean3, text1, text2, text3):
    SemigroupLawTester(
        semigroup=Map,
        value1={'sum': Sum(integer1), 'all': All(boolean1), 'first': First(text1)},
        value2={'sum': Sum(integer2), 'all': All(boolean2), 'first': First(text2)},
        value3={'sum': Sum(integer3), 'all': All(boolean3), 'first': First(text3)},
        result=Map({
            'sum': Sum(integer1 + integer2 + integer3),
            'all': All(boolean1 and boolean2 and boolean3),
            'first': First(text1)
        })
    ).test()


@given(integers(), text(), booleans(), dictionaries(keys=text(), values=integers()))
def test_fold(integer, text, boolean, dictionary):

    assert First(text).fold(identity) is text
    assert All(boolean).fold(identity) is boolean
    assert Sum(integers).fold(identity) is integers
    assert Map(dictionary).fold(identity) is dictionary
