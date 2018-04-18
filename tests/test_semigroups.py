from hypothesis import given
from hypothesis.strategies import text, integers, booleans, dictionaries

from testers.semigroup_law_tester import SemigroupLawTester
from testers.monoid_law_tester import MonoidLawTester

from pymonet.semigroups import Sum, All, One, First, Last, Map, Max, Min
from pymonet.utils import identity


@given(integers(), integers(), integers())
def test_sum_semigroup(x, y, z):
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


@given(integers(), integers(), integers())
def test_max_semigroup(x, y, z):
    SemigroupLawTester(
        semigroup=Max,
        value1=x,
        value2=y,
        value3=z,
        result=Max(max([x, y, z]))
    ).test()


@given(integers())
def test_max_monoid(integer):
    MonoidLawTester(
        monoid=Max,
        value=integer
    ).test()


@given(integers(), integers(), integers())
def test_min_semigroup(x, y, z):
    SemigroupLawTester(
        semigroup=Min,
        value1=x,
        value2=y,
        value3=z,
        result=Min(min([x, y, z]))
    ).test()


@given(integers())
def test_min_monoid(integer):
    MonoidLawTester(
        monoid=Min,
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


@given(booleans())
def test_all_monoid(boolean):
    MonoidLawTester(
        monoid=All,
        value=boolean
    ).test()


@given(booleans(), booleans(), booleans())
def test_one(bool1, bool2, bool3):
    SemigroupLawTester(
        semigroup=One,
        value1=bool1,
        value2=bool2,
        value3=bool3,
        result=One(bool1 or bool2 or bool3)
    ).test()


@given(booleans())
def test_one_monoid(boolean):
    MonoidLawTester(
        monoid=One,
        value=boolean
    ).test()


@given(text(), text(), text())
def test_first_semigroup(text1, text2, text3):
    SemigroupLawTester(
        semigroup=First,
        value1=text1,
        value2=text2,
        value3=text3,
        result=First(text1)
    ).test()


@given(text(), text(), text())
def test_last_semigroup(text1, text2, text3):
    SemigroupLawTester(
        semigroup=Last,
        value1=text1,
        value2=text2,
        value3=text3,
        result=Last(text3)
    ).test()


@given(
    integers(), integers(), integers(),
    booleans(), booleans(), booleans(),
    text(), text(), text()
)
def test_map(integer1, integer2, integer3, boolean1, boolean2, boolean3, text1, text2, text3):
    SemigroupLawTester(
        semigroup=Map,
        value1={
            'sum': Sum(integer1),
            'all': All(boolean1),
            'first': First(text1),
            'last': Last(text1),
            'min': Min(integer1),
            'max': Max(integer1)
        },
        value2={
            'sum': Sum(integer2),
            'all': All(boolean2),
            'first': First(text2),
            'last': Last(text2),
            'min': Min(integer2),
            'max': Max(integer2)
        },
        value3={
            'sum': Sum(integer3),
            'all': All(boolean3),
            'first': First(text3),
            'last': Last(text3),
            'min': Min(integer3),
            'max': Max(integer3)
        },
        result=Map({
            'sum': Sum(integer1 + integer2 + integer3),
            'all': All(boolean1 and boolean2 and boolean3),
            'first': First(text1),
            'last': Last(text3),
            'min': Min(min([integer1, integer2, integer3])),
            'max': Max(max([integer1, integer2, integer3]))
        })
    ).test()


@given(integers(), text(), booleans(), dictionaries(keys=text(), values=integers()))
def test_fold(integer, text, boolean, dictionary):

    assert First(text).fold(identity) is text
    assert All(boolean).fold(identity) is boolean
    assert Sum(integers).fold(identity) is integers
    assert Map(dictionary).fold(identity) is dictionary
