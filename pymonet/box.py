from typing import TypeVar, Generic, Callable


T = TypeVar('T')
U = TypeVar('U')


class Box(Generic[T]):
    """
    Data type for storage any type of data
    """

    def __init__(self, value: T) -> None:
        """
        :param value: value to store in Box
        :type value: Any
        """
        self.value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Box) and self.value == other.value

    def __str__(self) -> str:  # pragma: no cover
        return 'Box[value={}]'.format(self.value)

    def map(self, mapper: Callable[[T], U]) -> 'Box[U]':
        """
        Take function (A) -> b and applied this function on current box value and returns new box with mapped value.

        :param mapper: mapper function
        :type mapper: Function(A) -> B
        :returns: new box with mapped value
        :rtype: Box[B]
        """
        return Box(mapper(self.value))

    def bind(self, mapper: Callable[[T], U]) -> U:
        """
        Take function and applied this function on current box value and returns mapped value.

        :param mapper: mapper function
        :type mapper: Function(A) -> B
        :returns: new box with mapped value
        :rtype: B
        """
        return mapper(self.value)

    def ap(self, applicative):
        """
        Applies the function inside the Box[A] structure to another applicative type.

        :param applicative: applicative contains function
        :type applicative: Box[B]
        :returns: new Box with result of contains function
        :rtype: Box[A(B)]
        """
        return applicative.map(self.value)

    def to_maybe(self):
        """
        Transform Box into not empty Maybe.

        :returns: non empty Maybe monad with previous value
        :rtype: Maybe[A]
        """
        from pymonet.maybe import Maybe

        return Maybe.just(self.value)

    def to_either(self):
        """
        Transform Box into Right either.

        :returns: right Either monad with previous value
        :rtype: Right[A]
        """
        from pymonet.either import Right

        return Right(self.value)

    def to_lazy(self):
        """
        Transform Box into Lazy with returning value function.

        :returns: not folded Lazy monad with function returning previous value
        :rtype: Lazy[Function(() -> A)]
        """
        from pymonet.lazy import Lazy

        return Lazy(lambda: self.value)

    def to_try(self):
        """
        Transform Box into successfull Try.

        :returns: successfull Try monad with previous value
        :rtype: Try[A]
        """
        from pymonet.monad_try import Try

        return Try(self.value, is_success=True)

    def to_validation(self):
        """
        Transform Box into Validation.

        :returns: successfull Validation monad with previous value
        :rtype: Validation[A, []]
        """
        from pymonet.validation import Validation

        return Validation.success(self.value)
