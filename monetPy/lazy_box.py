class LazyBox:  # TODO add unit test

    def __init__(self, constructor_fn):
        self.constructor_fn = constructor_fn

    def map(self, fn):
        return LazyBox(lambda: fn(self.constructor_fn()))

    def fold(self, fn):
        return fn(self.constructor_fn())
