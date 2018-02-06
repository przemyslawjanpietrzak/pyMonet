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

    def __eq__(self, other):
        return self.value == other.value

    def fold(self, fn):
        return fn(self.value)

    @classmethod
    def neutral(cls):
        return cls(cls.neutral_element)


class Sum(Semigroup):

    neutral_element = 0

    def __str__(self):  # pragma: no cover
        return 'Sum[value={}]'.format(self.value)

    def concat(self, semigroup):
        return Sum(self.value + semigroup.value)


class All(Semigroup):

    neutral_element = True

    def __str__(self):  # pragma: no cover
        return 'All[value={}]'.format(self.value)

    def concat(self, semigroup):
        return All(self.value and semigroup.value)


class One(Semigroup):

    neutral_element = False

    def __str__(self):  # pragma: no cover
        return 'One[value={}]'.format(self.value)

    def concat(self, semigroup):
        return One(self.value or semigroup.value)


class First(Semigroup):

    def __str__(self):  # pragma: no cover
        return 'Fist[value={}]'.format(self.value)

    def concat(self, semigroup):
        return First(self.value)


class Map(Semigroup):

    def __str__(self):  # pragma: no cover
        return 'Map[value={}]'.format(self.value)

    def concat(self, semigroup):
        return Map(
            {key: value.concat(semigroup.value[key]) for key, value in self.value.items()}
        )
