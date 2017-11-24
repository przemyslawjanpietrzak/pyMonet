from hypothesis import given
from hypothesis.strategies import text, integers, booleans

from pymonet.semigroups import Sum, All, First, Map
from pymonet.utils import identity

ingredient1 = Map({'score': Sum(1), 'won': All(True), 'captain': First('captain america')})
ingredient2 = Map({'score': Sum(2), 'won': All(True), 'captain': First('iron man')})
ingredient3 = Map({'score': Sum(3), 'won': All(False), 'captain': First('Batman')})


@given(integers(), integers(), integers())
def test_sum(x, y, z):
    assert Sum(x).concat(Sum(y)) == Sum(x + y)
    assert Sum(x).concat(
        Sum(y).concat(Sum(z))
    ) == Sum(x + y + z)
    assert Sum(x).concat(Sum(y)).concat(Sum(z)) == Sum(x + y + z)


@given(booleans(), booleans(), booleans())
def test_all(bool1, bool2, bool3):

    assert All(bool1).concat(All(bool2)) == All(bool1 and bool2)
    assert All(bool1).concat(
        All(bool2).concat(All(bool3))
    ) == All(bool1 and bool2 and bool3)
    assert All(bool1).concat(All(bool2)).concat(All(bool3)) == All(bool1 and bool2 and bool3)


@given(text(), text(), text())
def test_first(text1, text2, text3):
    assert First(text1).concat(First(text2)) == First(text1)
    assert First(text1).concat(First(text2)).concat(First(text3)) == First(text1)
    assert First(text1).concat(
        First(text2).concat(First(text3))
    ) == First(text1)


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
