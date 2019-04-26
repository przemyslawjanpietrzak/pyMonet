class Semigroup:
    """
    In mathematics, a semigroup is an algebraic structure
    consisting of a set together with an associative binary operation.
    A semigroup generalizes a monoid in that there might not exist an identity element.
    It also (originally) generalized a group (a monoid with all inverses)
    to a type where every element did not have to have an inverse, this the name semigroup.
    """

    def __init__(self, value):
        self.value = value

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def fold(self, fn):
        return fn(self.value)

    @classmethod
    def neutral(cls):
        return cls(cls.neutral_element)


class Sum(Semigroup):
    """
    Sum is a Monoid that will combine 2 numbers under addition.
    """

    neutral_element = 0

    def __str__(self) -> str:  # pragma: no cover
        return 'Sum[value={}]'.format(self.value)

    def concat(self, semigroup: 'Sum') -> 'Sum':
        """
        :param semigroup: other semigroup to concat
        :type semigroup: Sum[B]
        :returns: new Sum with sum of concat semigroups values
        :rtype: Sum[A]
        """
        return Sum(self.value + semigroup.value)


class All(Semigroup):
    """
    All is a Monoid that will combine 2 values of any type using logical conjunction on their coerced Boolean values.
    """

    neutral_element = True

    def __str__(self) -> str:  # pragma: no cover
        return 'All[value={}]'.format(self.value)

    def concat(self, semigroup: 'All') -> 'All':
        """
        :param semigroup: other semigroup to concat
        :type semigroup: All[B]
        :returns: new All with last truly value or first falsy
        :rtype: All[A | B]
        """
        return All(self.value and semigroup.value)


class One(Semigroup):
    """
    One is a Monoid that will combine 2 values of any type using logical disjunction OR on their coerced Boolean values.
    """

    neutral_element = False

    def __str__(self) -> str:  # pragma: no cover
        return 'One[value={}]'.format(self.value)

    def concat(self, semigroup):
        """
        :param semigroup: other semigroup to concat
        :type semigroup: One[B]
        :returns: new One with first truly value or last falsy
        :rtype: One[A | B]
        """
        return One(self.value or semigroup.value)


class First(Semigroup):
    """
    First is a Monoid that will always return the first, value when 2 First instances are combined.
    """

    def __str__(self) -> str:  # pragma: no cover
        return 'Fist[value={}]'.format(self.value)

    def concat(self, semigroup):
        """
        :param semigroup: other semigroup to concat
        :type semigroup: First[B]
        :returns: new First with first value
        :rtype: First[A]
        """
        return First(self.value)


class Last(Semigroup):
    """
    Last is a Monoid that will always return the lastest, value when 2 Last instances are combined.
    """

    def __str__(self) -> str:  # pragma: no cover
        return 'Last[value={}]'.format(self.value)

    def concat(self, semigroup):
        """
        :param semigroup: other semigroup to concat
        :type semigroup: Last[B]
        :returns: new Last with last value
        :rtype: Last[A]
        """
        return Last(semigroup.value)


class Map(Semigroup):
    """
    Map is a Semigroup that will always return contated all values inside Map value
    """

    def __str__(self) -> str:  # pragma: no cover
        return 'Map[value={}]'.format(self.value)

    def concat(self, semigroup):
        """
        :param semigroup: other semigroup to concat
        :type semigroup: Map[B]
        :returns: new Map with concated all values
        :rtype: Map[A]
        """
        return Map(
            {key: value.concat(semigroup.value[key]) for key, value in self.value.items()}
        )


class Max(Semigroup):
    """
    Max is a Monoid that will combines 2 numbers, resulting in the largest of the two.
    """

    neutral_element = -float("inf")

    def __str__(self) -> str:  # pragma: no cover
        return 'Max[value={}]'.format(self.value)

    def concat(self, semigroup):
        """
        :param semigroup: other semigroup to concat
        :type semigroup: Max[B]
        :returns: new Max with largest value
        :rtype: Max[A | B]
        """
        return Max(self.value if self.value > semigroup.value else semigroup.value)


class Min(Semigroup):
    """
    Min is a Monoid that will combines 2 numbers, resulting in the smallest of the two.
    """

    neutral_element = float("inf")

    def __str__(self) -> str:  # pragma: no cover
        return 'Min[value={}]'.format(self.value)

    def concat(self, semigroup):
        """
        :param semigroup: other semigroup to concat
        :type semigroup: Min[B]
        :returns: new Min with smallest value
        :rtype: Min[A | B]
        """
        return Min(self.value if self.value <= semigroup.value else semigroup.value)
