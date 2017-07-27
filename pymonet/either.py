class Either:
    """
    The Either type represents values with two possibilities: B value of type Either<A, B> is either Left<A> or Right<B>
    But not both in the same time.
    """
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Either) and\
            self.value == other.value and\
            self.is_right() == other.is_right()

    def case(self, error, success):
        """
        takes 2 functions call only one of then with either value and return her result
        :params error: function to call when Either is Left
        :type (A) -> B
        :params success: function to call when Either is Right
        :type (A) -> B
        :return: B
        """
        if self.is_right():
            return success(self.value)
        return error(self.value)


class Left(Either):

    def map(self, _):
        """
        takes mapper function and return new instance of Left with the same value
        :return: Left<A>
        """
        return Left(self.value)

    def fold(self, _):
        """
        takes mapper function and return value of Left
        :return: A
        """
        return self.value

    def is_left(self):
        """
        :return: Boolean
        """
        return True

    def is_right(self):
        """
        :return: Boolean
        """
        return False


class Right(Either):

    def map(self, mapper):
        """
        takes mapper function and return new instance of Right with mapped value
        :param mapper: function to apply on Right value
        :type (A) -> B
        :return: Right<B>
        """
        return Right(mapper(self.value))

    def fold(self, mapper):
        """
        takes mapper function and returns result of them called with Right value
        :param mapper: function to apply on Right value
        :type (A) -> Either<B>
        :return: Either<B>
        """
        return mapper(self.value)

    def is_right(self):
        """
        :return: Boolean
        """
        return True

    def is_left(self):
        """
        :return: Boolean
        """
        return False
