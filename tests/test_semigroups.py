from hypothesis import given
from hypothesis.strategies import text, integers, booleans

from testers.semigroup_law_tester import SemigroupLawTester

from pymonet.semigroups import Sum, All, First, Map
from pymonet.utils import identity

ingredient1 = Map({'score': Sum(1), 'won': All(True), 'captain': First('captain america')})
ingredient2 = Map({'score': Sum(2), 'won': All(True), 'captain': First('iron man')})
ingredient3 = Map({'score': Sum(3), 'won': All(False), 'captain': First('Batman')})


@given(integers(), integers(), integers())
def test_sum(x, y, z):
    SemigroupLawTester(
        semigroup=Sum,
        value1=x,
        value2=y,
        value3=z,
        result=Sum(x + y + z)
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


@given(text(), text(), text())
def test_first(text1, text2, text3):
    SemigroupLawTester(
        semigroup=First,
        value1=text1,
        value2=text2,
        value3=text3,
        result=First(text1)
    ).test()


def test_map():
    assert ingredient1.concat(ingredient2) == Map(
        {'score': Sum(3), 'won': All(True), 'captain': First('captain america')}
    )

    assert ingredient1.concat(ingredient2).concat(ingredient3) == Map(
        {'score': Sum(6), 'won': All(False), 'captain': First('captain america')}
    )

    assert ingredient1.concat(ingredient2.concat(ingredient3)) == Map(
        {'score': Sum(6), 'won': All(False), 'captain': First('captain america')}
    )


@given(integers(), text(), booleans())
def test_fold(integer, text, boolean):

    dictionary = {'key': 'value'}

    assert First(text).fold(identity) is text
    assert All(boolean).fold(identity) is boolean
    assert Sum(integers).fold(identity) is integers
    assert Map(dictionary).fold(identity) is dictionary
