from typing import TypeVar, Generic, Callable, Union


T = TypeVar('T')
U = TypeVar('U')


class Maybe(Generic[T]):
    """
    Maybe type is the most common way of representing nothingness (or the null type).
    Maybe is effectively abstract and has two concrete subtypes: Box (also Some) and Nothing.
    """

    def __init__(self, value: T, is_nothing: bool) -> None:
        self.is_nothing = is_nothing
        if not is_nothing:
            self.value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Maybe) and \
            self.is_nothing == other.is_nothing and \
            (self.is_nothing or self.value == other.value)

    @classmethod
    def just(cls, value: T) -> 'Maybe[T]':
        """
        Create not empty maybe.

        :param mapper: value to store in Maybe
        :type mapper: Any
        :returns: Maybe[Any]
        """
        return Maybe(value, False)

    @classmethod
    def nothing(cls) -> 'Maybe[None]':
        """
        Create empty maybe.

        :returns: Maybe[None]
        """
        return Maybe(None, True)

    def map(self, mapper: Callable[[T], U]) -> Union['Maybe[U]', 'Maybe[None]']:
        """
        If Maybe is empty return new empty Maybe, in other case
        takes mapper function and returns new instance of Maybe
        with result of mapper.

        :param mapper: function to call with Maybe value
        :type mapper: Function(A) -> B
        :returns: Maybe[B | None]
        """
        if self.is_nothing:
            return Maybe.nothing()
        return Maybe.just(
            mapper(self.value)
        )

    def bind(self, mapper: Callable[[T], 'Maybe[U]']) -> Union['Maybe[U]', 'Maybe[None]']:
        """
        If Maybe is empty return new empty Maybe, in other case
        takes mapper function and returns result of mapper.

        :param mapper: function to call with Maybe.value
        :type mapper: Function(A) -> Maybe[B]
        :returns: Maybe[B | None]
        """
        if self.is_nothing:
            return Maybe.nothing()
        return mapper(self.value)

    def ap(self, applicative):
        """
        Applies the function inside the Maybe[A] structure to another applicative type for notempty Maybe.
        For empty returns copy of itself

        :param applicative: applicative contains function
        :type applicative: Maybe[B]
        :returns: new Maybe with result of contains function
        :rtype: Maybe[A(B) | None]
        """
        if self.is_nothing:
            return Maybe.nothing()
        return applicative.map(self.value)

    def filter(self, filterer: Callable[[T], bool]) -> Union['Maybe[T]', 'Maybe[None]']:
        """
        If Maybe is empty or filterer returns False return default_value, in other case
        return new instance of Maybe with the same value.

        :param filterer:
        :type filterer: Function(A) -> Boolean
        :returns: copy of self when filterer returns True, in other case empty Maybe
        :rtype: Maybe[A] | Maybe[None]
        """
        if self.is_nothing or not filterer(self.value):
            return Maybe.nothing()
        return Maybe.just(self.value)

    def get_or_else(self, default_value: U) -> Union[T, U]:
        """
        If Maybe is empty return default_value, in other case.

        :param default_value: value to return if Maybe is empty
        :type default_value: Any
        :returns: value of Maybe or default_value
        :rtype: A
        """
        if self.is_nothing:
            return default_value
        return self.value

    def to_either(self):
        """
        Transform Maybe to Either.

        :returns: Right monad with previous value when Maybe is not empty, in other case Left with None
        :rtype: Either[A | None]
        """
        from pymonet.either import Left, Right

        if self.is_nothing:
            return Left(None)
        return Right(self.value)

    def to_box(self):
        """
        Transform Maybe to Box.

        :returns: Box monad with previous value when Maybe is not empty, in other case Box with None
        :rtype: Box[A | None]
        """
        from pymonet.box import Box

        if self.is_nothing:
            return Box(None)
        return Box(self.value)

    def to_lazy(self):
        """
        Transform Maybe to Try.

        :returns: Lazy monad with function returning previous value in other case Left with None
        :rtype: Lazy[Function() -> (A | None)]
        """
        from pymonet.lazy import Lazy

        if self.is_nothing:
            return Lazy(lambda: None)
        return Lazy(lambda: self.value)

    def to_try(self):
        """
        Transform Maybe to Try.

        :returns: successfully Try with previous value when Maybe is not empty, othercase not successfully Try with None
        :rtype: Try[A]
        """
        from pymonet.monad_try import Try

        if self.is_nothing:
            return Try(None, is_success=False)
        return Try(self.value, is_success=True)

    def to_validation(self):
        """
        Transform Maybe into Validation.

        :returns: successfull Validation monad with previous value or None when Maybe is empty
        :rtype: Validation[A, []]
        """
        from pymonet.validation import Validation

        if self.is_nothing:
            return Validation.success(None)
        return Validation.success(self.value)
