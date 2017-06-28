class Semigroup:

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def fold(self, fn):
        return fn(self.value)


class Sum(Semigroup):

    def concat(self, semigroup):
        return Sum(self.value + semigroup.value)


class All(Semigroup):

    def concat(self, semigroup):
        return All(self.value and semigroup.value)


class First(Semigroup):

    def concat(self, semigroup):
        return First(self.value)


class Map(Semigroup):

    def concat(self, semigroup):
        return Map(
            {key: value.concat(semigroup.value[key]) for key, value in self.value.items()}
        )
