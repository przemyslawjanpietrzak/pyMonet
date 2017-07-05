class Try:

    def __init__(self, value, is_success):
        self.value = value
        self.is_success = is_success

    def __eq__(self, other):
        return self.value == other.value and self.is_success == other.is_success

    @classmethod
    def of(cls, fn, *args):
        try:
            return cls(fn(*args), True)
        except Exception as e:
            return cls(e, True)

    def map(self, mapper):
        if self.is_success:
            return Try(
                mapper(self.value),
                True
            )
        return Try(self.value, False)

    def fold(self, mapper):
        if self.is_success:
            return Try.of(mapper, self.value)
        return self.value

    def on_success(self, success_callback):
        if self.is_success:
            return success_callback(self.value)

    def on_fail(self, fail_callback):
        if not self.is_success:
            return fail_callback(self.value)

    def filter(self, filterer):
        pass