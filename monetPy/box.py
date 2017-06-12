class Box:

    def __init__(self, value):
        self.value = value

    def map(self, fn):
        return Box(fn(self.value))

    def fold(self, fn):
        return fn(self.value)
