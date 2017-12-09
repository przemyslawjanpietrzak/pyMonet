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

    def ap(self, monad):
        """
        It takes as a parameter another Box type which contains a function,
        and then applies that function to the value contained in the calling Box.
        :param monad: monad contains function
        :type Box[A -> B]
        :return: new Box with result of contains function
        :type Box[B]
        """
        return self.map(monad.value)

    def to_box(self):
        """
        Transform Either to Box
        :return Box monad with previous value
        :type Box[A]
        """
        from pymonet.box import Box

        return Box(self.value)

    def to_try(self):
        """
        Transform Either to Try
        :return resolved Try monad with previous value. Right is resolved successfully, Left not.
        :type Box[A]
        """
        from pymonet.monad_try import Try

        return Try(self.value, is_success=self.is_right())

    def to_lazy(self):
        """
        Transform Either to Try
        :return Lazy monad with function returning previous value
        :type Lazy[() -> A]
        """
        from pymonet.lazy import Lazy

        return Lazy(lambda: self.value)


class Left(Either):

    def map(self, _):
        """
        takes mapper function and return new instance of Left with the same value
        :return: Left<A>
        """
        return Left(self.value)

    def bind(self, _):
        """
        takes mapper function and return value of Left
        :return: A
        """
        return self

    def ap(self, monad):
        return Left(self.value)

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

    def to_maybe(self):
        """
        Transform Either to Maybe
        :return: Empty Maybe
        :type Maybe[None]
        """
        from pymonet.maybe import Maybe

        return Maybe.nothing()


class Right(Either):

    def map(self, mapper):
        """
        takes mapper function and return new instance of Right with mapped value
        :param mapper: function to apply on Right value
        :type (A) -> B
        :return: Right<B>
        """
        return Right(mapper(self.value))

    def bind(self, mapper):
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

    def to_maybe(self):
        """
        Transform Either to Maybe
        :return: Maybe with previous value
        :type Maybe[A]
        """
        from pymonet.maybe import Maybe

        return Maybe.just(self.value)
