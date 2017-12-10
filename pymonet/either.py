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
        Take 2 functions call only one of then with either value and return her result

        :params error: function to call when Either is Left
        :type error: (A) -> B
        :params success: function to call when Either is Right
        :type success: (A) -> B
        :returns: B
        """
        if self.is_right():
            return success(self.value)
        return error(self.value)

    def ap(self, monad):
        """
        Take as a parameter another Box type which contains a function,
        and then applies that function to the value contained in the calling Box.

        :param monad: monad contains function
        :type monad: Box[A -> B]
        :returns: new Box with result of contains function
        :rtype: Box[B]
        """
        return self.map(monad.value)

    def to_box(self):
        """
        Transform Either to Box
        :returns: Box monad with previous value
        :rtype: Box[A]
        """
        from pymonet.box import Box

        return Box(self.value)

    def to_try(self):
        """
        Transform Either to Try

        :returns: resolved Try monad with previous value. Right is resolved successfully, Left not.
        :rtype: Box[A]
        """
        from pymonet.monad_try import Try

        return Try(self.value, is_success=self.is_right())

    def to_lazy(self):
        """
        Transform Either to Try
        :returns: Lazy monad with function returning previous value
        :type Lazy[() -> A]
        """
        from pymonet.lazy import Lazy

        return Lazy(lambda: self.value)


class Left(Either):
    """
    Successfully Either
    """

    def map(self, _):
        """
        Take mapper function and return new instance of Left with the same value.

        :returns: Copy of self
        :rtype: Left<A>
        """
        return Left(self.value)

    def bind(self, _):
        """
        Take mapper function and return value of Left.

        :returns: Stored value
        :rtype: A
        """
        return self

    def ap(self, monad):
        """
        :returns: Copy of self
        :rtype: Left<A>
        """
        return Left(self.value)

    def is_left(self):
        """
        :returns: True
        :rtype: Boolean
        """
        return True

    def is_right(self):
        """
        :returns: False
        :rtype: Boolean
        """
        return False

    def to_maybe(self):
        """
        Transform Either to Maybe.

        :returns: Empty Maybe
        :rtype: Maybe<None>
        """
        from pymonet.maybe import Maybe

        return Maybe.nothing()


class Right(Either):
    """
    Not successfully Either
    """

    def map(self, mapper):
        """
        Take mapper function and return new instance of Right with mapped value.
|
        :param mapper: function to apply on Right value
        :type mapper: Function(A) -> B
        :returns: Right<B>
        """
        return Right(mapper(self.value))

    def bind(self, mapper):
        """
        Take mapper function and returns result of them called with Right value.

        :param mapper: function to apply on Right value
        :type mapper: Function(A) -> Either<B>
        :returns: Either<B>
        """
        return mapper(self.value)

    def is_right(self):
        """
        :returns: True
        :rtype: Boolean
        """
        return True

    def is_left(self):
        """
        :returns: False
        :rtype: Boolean
        """
        return False

    def to_maybe(self):
        """
        Transform Either to Maybe.

        :returns: Maybe with previous value
        :type Maybe<A>
        """
        from pymonet.maybe import Maybe

        return Maybe.just(self.value)
