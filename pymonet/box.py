class Box:
    """
    Data type for storage any type of data
    """

    def __init__(self, value):
        """
        :param value: value to store in Box
        :type value: Any
        """
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def map(self, mapper):
        """
        takes function (a) -> b and applied this function on current box value and returns new box with mapped value
        :param mapper: mapper function
        :type mapper: (a) -> b
        :returns: new box with mapped value
        :rtype: Box<b>
        """
        return Box(mapper(self.value))

    def bind(self, mapper):
        """
        takes function (a) -> b and applied this function on current box value and returns mapped value
        :param mapper: mapper function
        :type mapper: (a) -> b
        :returns: new box with mapped value
        :rtype: b
        """
        return mapper(self.value)

    def ap(self, monad):
        """
        It takes as a parameter another Box type which contains a function,
        and then applies that function to the value contained in the calling Box.
        :param monad: monad contains function
        :type monad: Box[A -> B]
        :returns: new Box with result of contains function
        :rtype: Box[B]
        """
        return self.map(monad.value)

    def to_maybe(self):
        """
        :returns: non empty Maybe monad with previous value
        :rtype: Maybe[A]
        """
        from pymonet.maybe import Maybe

        return Maybe.just(self.value)

    def to_either(self):
        """
        :returns: right Either monad with previous value
        :rtype: Right[A]
        """
        from pymonet.either import Right

        return Right(self.value)

    def to_lazy(self):
        """
        :returns: not folded Lazy monad with function returning previous value
        """
        from pymonet.lazy import Lazy

        return Lazy(lambda: self.value)

    def to_try(self):
        """
        :returns: successfully Try monad with previous value
        """
        from pymonet.monad_try import Try

        return Try(self.value, is_success=True)
