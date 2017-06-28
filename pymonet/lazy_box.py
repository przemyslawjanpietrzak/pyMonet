class LazyBox:
    """
     Data type for storage any type of function.
     This function (and all his mappers) will be called only during calling fold method
     """

    def __init__(self, constructor_fn):
        """
        :param constructor_fn: function to call during fold method call
        """
        self.constructor_fn = constructor_fn

    def map(self, fn):
        """
        takes function (A) -> A and returns new LazyBox with mapped argument of LazyBox constructor function.
        Both mapper end constructor will be called only during calling fold method
        :param fn: mapper function
        :type   (constructor_fn) -> B
        :return: Lazybox<() -> fn(constructor_fn)>
        """
        return LazyBox(lambda: fn(self.constructor_fn()))

    def fold(self, fn):
        """
        takes function and call constructor function passing returned value to fn function.
        It's only way to call function store in LazyBox
        :param fn: (constructor_fn) -> B
        :return: B
        """
        return fn(self.constructor_fn())
