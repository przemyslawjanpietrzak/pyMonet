from pymonet.semigroups import Sum, All, First, Map
from pymonet.utils import identity

ingredient1 = Map({'score': Sum(1), 'won': All(True), 'captain': First('captain america')})
ingredient2 = Map({'score': Sum(2), 'won': All(True), 'captain': First('iron man')})
ingredient3 = Map({'score': Sum(3), 'won': All(False), 'captain': First('Batman')})


def test_sum():
    assert Sum(1).concat(Sum(2)) == Sum(3)
    assert Sum(1).concat(
        Sum(2).concat(Sum(3))
    ) == Sum(6)
    assert Sum(1).concat(Sum(2)).concat(Sum(3)) == Sum(6)


def test_all():
    assert All(True).concat(All(True)) == All(True)
    assert All(True).concat(All(False)) == All(False)

    assert All(True).concat(
        All(True).concat(All(True))
    ) == All(True)
    assert All(True).concat(All(True)).concat(All(True)) == All(True)

    assert All(True).concat(
        All(False).concat(All(True))
    ) == All(False)
    assert All(True).concat(All(True)).concat(All(False)) == All(False)


def test_first():
    assert First('first').concat(First('second')) == First('first')
    assert First('first').concat(First('second')).concat(First('third')) == First('first')
    assert First('first').concat(
        First('second').concat(First('third'))
    ) == First('first')


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


def test_fold():

    dictionary = {'key': 'value'}

    assert First('first').fold(identity) is 'first'
    assert All('all').fold(identity) is 'all'
    assert Sum('sum').fold(identity) is 'sum'
    assert Map(dictionary).fold(identity) is dictionary
