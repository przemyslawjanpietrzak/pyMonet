class Either:

    def __init__(self, value):
        self.value = value


class Left(Either):

    def map(self, left_fn, right_fn):
        return Left(left_fn(self.value))

    def fold(self, left_fn, right_fn):
        return left_fn(self.value)


class Right(Either):

    def map(self, left_fn, right_fn):
        return Right(right_fn(self.value))

    def fold(self, left_fn, right_fn):
        return right_fn(self.value)