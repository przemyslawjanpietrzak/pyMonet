class Reader:

    def __init__(self, constructor_fn):
        self.fn = constructor_fn

    @classmethod
    def of(cls, value):
        def lambda_fn(*args):
            return value

        return Reader(lambda_fn)

    def map(self, mapper):
        def lambda_fn(*args):
            return mapper(self.get(*args))

        return Reader(lambda_fn)

    def bind(self, folder):
        def lambda_fn(*args):
            return folder(self.get(*args)).get(*args)

        return Reader(lambda_fn)

    def get(self, *args):
        return self.fn(*args)

    # def ap(self, applicative):
    #     def lambda_fn(fn):
    #         return Reader(lambda value: fn(self.get(value)))
    #     # def lambda_fn(*args):
    #     #     return applicative.get(self.get(*args)
    # return applicative.bind(lambda_fn)

    def to_box(self, *args):
        from pymonet.box import Box

        return Box(self.fn(args))

    def to_maybe(self, *args):
        from pymonet.maybe import Maybe

        return Maybe.just(self.fn(args))
    
    def to_either(self, *args):
        from pymonet.either import Right

        return Right(self.fn(*args))
