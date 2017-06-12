class LazyBox: #  TODO add unit test

    def __init__(self, value):
        self.value = value

    def map(self, fn):
        return LazyBox(lambda: fn(self.value()))

    def fold(self, fn):
        return lambda: fn(self.value())
