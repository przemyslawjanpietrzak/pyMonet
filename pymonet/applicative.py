class Applicative:
    """
     Data type for storage any type of function.
     This function (and all his mappers) will be called only during calling fold method
     """

    def __init__(self, constructor_fn):
        """
        :param constructor_fn: function to call during fold method call
        """
        self.constructor_fn = constructor_fn

    def map(self, mapper):
        """
        takes function (A) -> A and returns new Applicative with mapped argument of Applicative constructor function.
        Both mapper end constructor will be called only during calling fold method
        :param mapper: mapper function
        :type   (constructor_mapper) -> B
        :return: Applicative<() -> mapper(constructor_fn)>
        """
        return Applicative(lambda *args: mapper(self.constructor_fn(*args)))

    def fold(self, fn, *args):
        """
        takes function and call constructor function passing returned value to fn function.
        It's only way to call function store in Applicative
        :param fn: (constructor_fn) -> B
        :return: B
        """
        return fn(self.constructor_fn(*args))
