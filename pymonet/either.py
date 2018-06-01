from typing import TypeVar, Generic, Callable, Any


T = TypeVar('T')
U = TypeVar('U')


class Either(Generic[T]):
    """
    The Either type represents values with two possibilities: B value of type Either[A, B] is either Left[A or Right[B]
    But not both in the same time.
    """

    def __init__(self, value: T) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Either) and\
            self.value == other.value and\
            self.is_right() == other.is_right()

    def case(self, error: Callable[[T], U], success: Callable[[T], U]) -> U:
        """
        Take 2 functions call only one of then with either value and return her result.

        :params error: function to call when Either is Left
        :type error: Function(A) -> B
        :params success: function to call when Either is Right
        :type success: Function(A) -> B
        :returns: result of success handler when Eihter is Right, result of error handler when Eihter is Left
        :rtpye: B
        """
        if self.is_right():
            return success(self.value)
        return error(self.value)

    def ap(self, applicative):
        """
        Applies the function inside the Either[A] structure to another applicative type.

        :param applicative: applicative contains function
        :type applicative: Either[B]
        :returns: new Either with result of contains function
        :rtype: Either[A(B)]
        """
        return applicative.map(self.value)

    def to_box(self):
        """
        Transform Either to Box.

        :returns: Box monad with previous value
        :rtype: Box[A]
        """
        from pymonet.box import Box

        return Box(self.value)

    def to_try(self):
        """
        Transform Either to Try.

        :returns: resolved Try monad with previous value. Right is resolved successfully, Left not.
        :rtype: Box[A]
        """
        from pymonet.monad_try import Try

        return Try(self.value, is_success=self.is_right())

    def to_lazy(self):
        """
        Transform Either to Try.

        :returns: Lazy monad with function returning previous value
        :rtype: Lazy[Function() -> A]
        """
        from pymonet.lazy import Lazy

        return Lazy(lambda: self.value)

    def is_right(self):
        pass


class Left(Either, Generic[T]):
    """Not successfully Either"""

    def map(self, _: Callable[[Any], Any]) -> 'Left[T]':
        """
        Take mapper function and return new instance of Left with the same value.

        :returns: Copy of self
        :rtype: Left[A]
        """
        return Left(self.value)

    def bind(self, _) -> 'Left[T]':
        """
        Take mapper function and return value of Left.

        :returns: Stored value
        :rtype: A
        """
        return self

    def ap(self, monad):
        """
        :returns: Copy of self
        :rtype: Left[A]
        """
        return Left(self.value)

    def is_left(self) -> bool:
        """
        :returns: True
        :rtype: Boolean
        """
        return True

    def is_right(self) -> bool:
        """
        :returns: False
        :rtype: Boolean
        """
        return False

    def to_maybe(self):
        """
        Transform Either to Maybe.

        :returns: Empty Maybe
        :rtype: Maybe[None]
        """
        from pymonet.maybe import Maybe

        return Maybe.nothing()

    def to_validation(self):
        """
        Transform Box into Validation.

        :returns: failed Validation monad with previous value as error
        :rtype: Validation[None, [A]]
        """
        from pymonet.validation import Validation

        return Validation.fail([self.value])


class Right(Either):
    """Not successfully Either"""

    def map(self, mapper: Callable[[T], U]) -> Either[U]:
        """
        Take mapper function and return new instance of Right with mapped value.

        :param mapper: function to apply on Right value
        :type mapper: Function(A) -> B
        :returns: new Right with result of mapper
        :rtype: Right[B]
        """
        return Right(mapper(self.value))

    def bind(self, mapper: Callable[[T], U]) -> U:
        """
        Take mapper function and returns result of them called with Right value.

        :param mapper: function to apply on Right value
        :type mapper: Function(A) -> Either[B]
        :returns: result of mapper
        :rtype: Either[B]
        """
        return mapper(self.value)

    def is_right(self) -> bool:
        """
        :returns: True
        :rtype: Boolean
        """
        return True

    def is_left(self) -> bool:
        """
        :returns: False
        :rtype: Boolean
        """
        return False

    def to_maybe(self):
        """
        Transform Either to Maybe.

        :returns: Maybe with previous value
        :rtype: Maybe[A]
        """
        from pymonet.maybe import Maybe

        return Maybe.just(self.value)

    def to_validation(self):
        """
        Transform Either into Validation.

        :returns: successfull Validation monad with previous value
        :rtype: Validation[A, []]
        """
        from pymonet.validation import Validation

        return Validation.success(self.value)
