from typing import TypeVar, Generic, Callable


T = TypeVar('T')
U = TypeVar('U')
W = TypeVar('W')


class Lazy(Generic[T, U]):
    """
    Data type for storage any type of function.
    This function (and all his mappers) will be called only during calling fold method
    """

    def __init__(self, constructor_fn: Callable[[T], U]) -> None:
        """
        :param constructor_fn: function to call during fold method call
        :type constructor_fn: Function() -> A
        """
        self.constructor_fn = constructor_fn
        self.is_evaluated = False
        self.value = None

    def __str__(self) -> str:  # pragma: no cover
        return 'Lazy[fn={}, value={}, is_evaluated={}]'.format(self.constructor_fn, self.value, self.is_evaluated)

    def __eq__(self, other: object) -> bool:
        """
        Two Lazy are equals where both are evaluated both have the same value and constructor functions.
        """
        return (
            isinstance(other, Lazy)
            and self.is_evaluated == other.is_evaluated
            and self.value == other.value
            and self.constructor_fn == other.constructor_fn
        )

    @classmethod
    def of(cls, value: U) -> 'Lazy[T, U]':
        """
        Returns Lazy with function returning argument.

        :param value: value to return by Lazy constructor_fn
        :type value: Any
        :returns: Lazy with function returning argument
        :rtype: Lazy[Function() -> A]
        """
        return Lazy(lambda *args: value)

    def _compute_value(self, *args):
        self.is_evaluated = True
        self.value = self.constructor_fn(*args)

        return self.value

    def map(self, mapper: Callable[[U], W]) -> 'Lazy[T, W]':
        """
        Take function Function(A) -> B and returns new Lazy with mapped result of Lazy constructor function.
        Both mapper end constructor will be called only during calling fold method.

        :param mapper: mapper function
        :type mapper: Function(A) -> B
        :returns: Lazy with mapped value
        :rtype: Lazy[Function() -> B)]
        """
        return Lazy(lambda *args: mapper(self.constructor_fn(*args)))

    def ap(self, applicative):
        """
        Applies the function inside the Lazy[A] structure to another applicative type for notempty Lazy.
        For empty returns copy of itself

        :param applicative: applicative contains function
        :type applicative: Lazy[Function(A) -> B]
        :returns: new Lazy with result of contains function
        :rtype: Lazy[B]
        """
        return Lazy(lambda *args: self.constructor_fn(applicative.get(*args)))

    def bind(self, fn: 'Callable[[U], Lazy[U, W]]') -> 'Lazy[T, W]':
        """
        Take function and call constructor function passing returned value to fn function.

        It's only way to call function store in Lazy
        :param fn: Function(constructor_fn) -> B
        :returns: result od folder function
        :rtype: B
        """
        def lambda_fn(*args):
            computed_value = self._compute_value(*args)
            return fn(computed_value).constructor_fn

        return Lazy(lambda_fn)

    def get(self, *args):
        """
        Evaluate function and memoize her output or return memoized value when function was evaluated.

        :returns: result of function in Lazy
        :rtype: A
        """
        if self.is_evaluated:
            return self.value
        return self._compute_value(*args)

    def to_box(self, *args):
        """
        Transform Lazy into Box with constructor_fn result.

        :returns: Box monad with constructor_fn result
        :rtype: Box[A]
        """
        from pymonet.box import Box

        return Box(self.get(*args))

    def to_either(self, *args):
        """
        Transform Lazy into Either (Right) with constructor_fn result.

        :returns: Right monad with constructor_fn result
        :rtype: Right[A]
        """
        from pymonet.either import Right

        return Right(self.get(*args))

    def to_maybe(self, *args):
        """
        Transform Lazy into not empty Maybe with constructor_fn result.

        :returns: not empty Maybe monad with constructor_fn result
        :rtype: Maybe[A]
        """
        from pymonet.maybe import Maybe

        return Maybe.just(self.get(*args))

    def to_try(self, *args):
        """
        Transform Lazy into Try with constructor_fn result.
        Try will be successful only when constructor_fn not raise anything.

        :returns: Try with constructor_fn result
        :rtype: Try[A] | Try[Error]
        """
        from pymonet.monad_try import Try

        return Try.of(self.constructor_fn, *args)

    def to_validation(self, *args):
        """
        Transform Lazy into successful Validation with constructor_fn result.

        :returns: successfull Validation monad with previous value
        :rtype: Validation[A, []]
        """
        from pymonet.validation import Validation

        return Validation.success(self.get(*args))
