class Try:

    def __init__(self, value, is_success):
        self.value = value
        self.is_success = is_success

    def __eq__(self, other):
        return isinstance(other, type(self))\
            and self.value == other.value\
            and self.is_success == other.is_success

    @classmethod
    def of(cls, fn, *args):
        try:
            return cls(fn(*args), True)
        except Exception as e:
            return cls(e, False)

    def map(self, mapper):
        if self.is_success:
            return Try(mapper(self.value), True)
        return Try(self.value, False)

    def fold(self, mapper):
        if self.is_success:
            return mapper(self.value)
        return self

    def on_success(self, success_callback):
        if self.is_success:
            success_callback(self.value)
        return self

    def on_fail(self, fail_callback):
        if not self.is_success:
            fail_callback(self.value)
        return self

    def filter(self, filterer):
        if self.is_success and filterer(self.value):
            return Try(self.value, True)
        return Try(self.value, False)

    def get(self):
        return self.value

    def get_or_else(self, default_value):
        if self.is_success:
            return self.value
        return default_value
