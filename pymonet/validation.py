class Validation:
    """It that can hold either a success value or a failure value and has methods for accumulating errors"""

    def __init__(self, value, errors):
        self.value = value
        self.errors = errors

    def __eq__(self, other):
        """
        Two Validations are equals when values and errors lists are equal.
        """
        return (isinstance(other, Validation) and
                self.errors == other.errors and
                self.value == other.value)

    def __str__(self):  # pragma: no cover
        if self.is_success():
            return 'Validation.success[{}]'.format(self.value)
        return 'Validation.fail[{}, {}]'.format(self.value, self.errors)

    @classmethod
    def success(cls, value=None):
        """
        Returns successful Validation with value and empty errors list.

        :params value: value to store in Validation
        :type value: A
        :returns: Successful Validation
        :rtype: Validation[A, []]
        """
        return Validation(value, [])

    @classmethod
    def fail(cls, errors=[]):
        """
        Returns failed Validation with None as value and errors list.

        :params errors: list of errors to store
        :type value: List[E]
        :returns: Failed Validation
        :rtype: Validation[None, List[E]]
        """
        return Validation(None, errors)

    def is_success(self):
        """
        Returns True when errors list are empty.

        :returns: True for empty errors list
        :rtype: Boolean
        """
        return len(self.errors) == 0

    def is_fail(self):
        """
        Returns True when errors list are not empty.

        :returns: True for empty errors not list
        :rtype: Boolean
        """
        return len(self.errors) != 0

    def map(self, mapper):
        """
        Take function (A) -> B and applied this function on current Validation value.

        :param mapper: mapper function
        :type mapper: Function(A) -> B
        :returns: new Validation with mapped value and previous errors
        :rtype: Validation[B, List[E]]
        """
        return Validation(mapper(self.value), self.errors)

    def bind(self, folder):
        """
        Take function and applied this function on current Validation value and returns folder result.

        :param mapper: mapper function
        :type mapper: Function(A) -> Validation[B, E]
        :returns: new Validation with mapped value
        :rtype: Validation[B, E]
        """
        return folder(self.value)

    def ap(self, fn):
        """
        It takes as a parameter function returning another Validation.
        Function is called with Validation value and returns new Validation with previous value
        and concated new and old errors.

        :param monad: monad contains function
        :type monad: Function(A) -> Validation[Any, List[E]]
        :returns: new validation with stored errors
        :rtype: Validation[A, List[E]]
        """
        return Validation(self.value, self.errors + fn(self.value).errors)

    def to_either(self):
        """
        Transform Validation to Either.

        :returns: Right monad with previous value when Validation has no errors, in other case Left with errors list
        :rtype: Right[A] | Left[E]
        """
        from pymonet.either import Left, Right

        if self.is_success():
            return Right(self.value)
        return Left(self.errors)

    def to_maybe(self):
        """
        Transform Validation to Maybe.

        :returns: Maybe with Validation Value when Validation has no errors, in other case empty Maybe
        :rtype: Maybe[A | None]
        """
        from pymonet.maybe import Maybe

        if self.is_success():
            return Maybe.just(self.value)
        return Maybe.nothing()

    def to_box(self):
        """
        Transform Validation to Box.

        :returns: Box with Validation value
        :rtype: Box[A]
        """
        from pymonet.box import Box

        return Box(self.value)

    def to_lazy(self):
        """
        Transform Validation to Try.

        :returns: Lazy monad with function returning Validation value
        :rtype: Lazy[Function() -> (A | None)]
        """
        from pymonet.lazy import Lazy

        return Lazy(lambda: self.value)

    def to_try(self):
        """
        Transform Validation to Try.

        :returns: successfully Try with Validation value value. Try is successful when Validation has no errors
        :rtype: Try[A]
        """
        from pymonet.monad_try import Try

        return Try(self.value, is_success=self.is_success())
