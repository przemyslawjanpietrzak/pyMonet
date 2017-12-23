class Validation:
    
    def __init__(self, value, success):
        self.value = value
        self.success = success

    def __eq__(self, other):
        return (isinstance(other, Validation) and 
            self.success == other.success and
            self.value == other.value)

    @classmethod
    def success(cls, value=None):
        return Validation(value, True)

    @classmethod
    def fail(cls, value):
        return Validation(value, False)

    def is_success(self):
        return self.success

    def is_fail(self):
        return not self.success

    def map(self, mapper):
        if self.success:
            return Validation.success(mapper(self.value))
        return Validation.fail(self.value)

    def bind(self, folder):
        if self.success:
            return folder(self.value)
        return Validation.fail(self.value)

    def ap(self, fn):
        fn_result = fn(self.value)
        if fn_result.is_success():
            if self.success:
                return Validation.success(self.value)
            return Validation.fail(fn_result.value)
        if self.success:
            return Validation.fail(fn_result.value)
        return Validation.fail(self.value + fn_result.value)

    def to_either(self):
        from pymonet.either import Left, Right

        if self.success:
            return Right(self.value)
        return Left(self.value)

    def to_box(self):
        from pymonet.box import Box

        return Box(self.value)

    def to_lazy(self):
        from pymonet.lazy import Lazy

        return Lazy(lambda: self.value)

    def to_try(self):
        from pymonet.monad_try import Try

        if self.success:
            return Try(self.value, is_success=True)
        return Try(self.value, is_success=False)
