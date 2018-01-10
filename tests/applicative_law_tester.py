from pymonet.utils import identity


class ApplicativeLawTester:

    def __init__(self, applicative, value, mapper1, mapper2, get_fn=identity):
        self.applicative = applicative
        self.value = value
        self.mapper1 = mapper1
        self.mapper2 = mapper2
        self.get_fn = get_fn

    def _assert(self, x, y):
        assert self.get_fn(x) == self.get_fn(y)

    def identity_test(self):
        x = self.applicative(identity).ap(self.applicative(self.value))
        y = self.applicative(self.value)

        self._assert(x, y)

    def composition_test(self):
        def lambda_fn(fn1):
            return lambda fn2: lambda value: fn1(fn2(value))

        x = self.applicative(lambda_fn)\
                .ap(self.applicative(self.mapper1))\
                .ap(self.applicative(self.mapper2))\
                .ap(self.applicative(self.value))
        y = self.applicative(self.mapper1).ap(
            self.applicative(self.mapper2).ap(self.applicative(self.value))
            )

        self._assert(x, y)

    def homomorphism_test(self):
        x = self.applicative(self.mapper1).ap(self.applicative(self.value))
        y = self.applicative(
            self.mapper1(self.value)
        )
        self._assert(x, y)

    def interchange_test(self):
        x = self.applicative(self.mapper1).ap(self.applicative(self.value))
        y = self.applicative(lambda fn: fn(self.value)).ap(
            self.applicative(self.mapper1)
        )
        self._assert(x, y)

    def test(self):
        self.identity_test()
        self.composition_test()
        self.homomorphism_test()
        self.interchange_test()
