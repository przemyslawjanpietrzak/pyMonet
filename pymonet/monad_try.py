from typing import Callable


class Try:
    """
    The Try control gives us the ability write safe code
    without focusing on try-catch blocks in the presence of exceptions.
    """

    def __init__(self, value, is_success: bool) -> None:
        self.value = value
        self.is_success = is_success

    def __eq__(self, other) -> bool:
        return isinstance(other, type(self))\
            and self.value == other.value\
            and self.is_success == other.is_success

    def __str__(self) -> str:  # pragma: no cover
        return 'Try[value={}, is_success={}]'.format(self.value, self.is_success)

    @classmethod
    def of(cls, fn: Callable, *args):
        """
        Call argument function with args in try-catch.
        when function don't raise exception, not successfully when raise.

        :params fn: function to call and store in monad
        :type fn: Function(*args) -> A
        :params *args:
        :type fn: List
        :retruns: Successfully monad Try when function don't raise exception, not successfully when raise
        :rtype: Try[A]
        """
        try:
            return cls(fn(*args), True)
        except Exception as e:
            return cls(e, False)

    def map(self, mapper):
        """
        Take function and applied this function with monad value and returns new monad with mapped value.

        :params mapper: function to apply on monad value
        :type mapper: Function(A) -> B
        :returns: for successfully new Try with mapped value, othercase copy of self
        :rtype: Try[B]
        """
        if self.is_success:
            return Try(mapper(self.value), True)
        return Try(self.value, False)

    def bind(self, binder):
        """
        Take function and applied this function with monad value and returns function result.

        :params binder: function to apply on monad value
        :type binder: Function(A) -> Try[B]
        :returns: for successfully result of binder, othercase copy of self
        :rtype: Try[B]
        """
        if self.is_success:
            return binder(self.value)
        return self

    def on_success(self, success_callback):
        """
        Call success_callback function with monad value when monad is successfully.

        :params success_callback: function to apply with monad value.
        :type success_callback: Function(A)
        :returns: self
        :rtype: Try[A]
        """
        if self.is_success:
            success_callback(self.value)
        return self

    def on_fail(self, fail_callback):
        """
        Call success_callback function with monad value when monad is not successfully.

        :params fail_callback: function to apply with monad value.
        :type fail_callback: Function(A)
        :returns: self
        :rtype: Try[A]
        """
        if not self.is_success:
            fail_callback(self.value)
        return self

    def filter(self, filterer):
        """
        Take filterer function, when monad is successfully call filterer with monad value.
        When filterer returns True method returns copy of monad, othercase
        not successfully Try with previous value.

        :params filterer: function to apply on monad value
        :type filterer: Function(A) -> Boolean
        :returns: Try with previous value
        :rtype: Try[A]
        """
        if self.is_success and filterer(self.value):
            return Try(self.value, True)
        return Try(self.value, False)

    def get(self):
        """
        Return monad value.

        :returns: monad value
        :rtype: A
        """
        return self.value

    def get_or_else(self, default_value):
        """
        Return monad value when is successfully.
        Othercase return default_value argument.

        :params default_value: value to return when monad is not successfully.
        :type default_value: B
        :returns: monad value
        :rtype: A | B
        """
        if self.is_success:
            return self.value
        return default_value
