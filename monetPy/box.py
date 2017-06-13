class Box:

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def map(self, fn):
        return Box(fn(self.value))

    def fold(self, fn):
        return fn(self.value)
