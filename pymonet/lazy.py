class Lazy:
    """
     Data type for storage any type of function.
     This function (and all his mappers) will be called only during calling fold method
     """

    def __init__(self, constructor_fn):
        """
        :param constructor_fn: function to call during fold method call
        """
        self.constructor_fn = constructor_fn
        self.is_evaluated = False
        self.value = None

    def __eq__(self, other):
        """
        Two Lazy are equals where both are evaluated both have the same value and constructor functions
        """
        return (
            isinstance(other, Lazy)
            and self.is_evaluated == other.is_evaluated
            and self.value == other.value
            and self.constructor_fn == other.constructor_fn
        )

    def _compute_value(self, *args):
        self.is_evaluated = True
        self.value = self.constructor_fn(*args)
        return self.value

    def map(self, mapper):
        """
        takes function (A) -> A and returns new Lazy with mapped argument of Lazy constructor function.
        Both mapper end constructor will be called only during calling fold method
        :param mapper: mapper function
        :type   (constructor_mapper) -> B
        :return: Lazy<() -> mapper(constructor_fn)>
        """
        return Lazy(lambda *args: mapper(self.constructor_fn(*args)))

    def fold(self, fn, *args):
        """
        takes function and call constructor function passing returned value to fn function.
        It's only way to call function store in Lazy
        :param fn: (constructor_fn) -> B
        :return: B
        """
        return fn(self._compute_value(*args))

    def get(self, *args):
        """
        Evaluate function and memoize her output or return memoized value when function was evaluated
        :return: A
        """
        if self.is_evaluated:
            return self.value
        return self._compute_value(*args)
