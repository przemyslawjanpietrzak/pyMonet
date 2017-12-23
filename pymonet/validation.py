class Validation:
    
    def __init__(self, value, errors):
        self.value = value
        self.errors = errors

    def __eq__(self, other):
        return (isinstance(other, Validation) and 
            self.errors == other.errors and
            self.value == other.value)

    def __str__(self):
        if self.is_success():
            return 'Validation.success[{}]'.format(self.value)
        return 'Validation.fail[{}, {}]'.format(self.value, self.errors)

    @classmethod
    def success(cls, value=None):
        return Validation(value, [])

    @classmethod
    def fail(cls, errors=[]):
        return Validation(None, errors)

    def is_success(self):
        return len(self.errors) == 0

    def is_fail(self):
        return len(self.errors) != 0

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
        return Validation(self.value, self.errors + fn_result.errors)

    def to_either(self):
        from pymonet.either import Left, Right

        if self.is_success():
            return Right(self.value)
        return Left(self.errors)

    def to_box(self):
        from pymonet.box import Box

        return Box(self.value)

    def to_lazy(self):
        from pymonet.lazy import Lazy

        return Lazy(lambda: self.value)

    def to_try(self):
        from pymonet.monad_try import Try

        if self.is_success():
            return Try(self.value, is_success=True)
        return Try(self.value, is_success=False)
