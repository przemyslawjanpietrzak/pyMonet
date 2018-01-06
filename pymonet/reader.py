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
