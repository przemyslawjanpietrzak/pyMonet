from pymonet.utils import identity


class ApplicativeLawTester:

    def __init__(self, applicative, value, mapper1, mapper2):
        self.applicative = applicative
        self.value = value
        self.mapper1 = mapper1
        self.mapper2 = mapper2

    def get_identity_test(self):
        assert self.applicative(identity).ap(self.applicative(self.value)) == self.applicative(self.value)

    def get_composition_test(self):

        def lambda_fn(f):
            lambda g: lambda x: f(g(x))

        x = self.applicative(lambda_fn)\
            .ap(self.applicative(self.mapper1))\
            .ap(self.applicative(self.mapper2))\
            .ap(self.applicative(lambda: self.applicative))
        y = self.applicative(self.mapper1).ap(
            self.applicative(self.mapper2).ap(self.applicative(lambda: self.applicative))
        )

        assert x == y

        # x = (A.of (f) -> (g) -> (x) -> f (g x)).ap(A.of g).ap(A.of h).ap(A.of a)
        # y = (A.of g).ap((A.of h).ap(A.of a))

    def get_homomorphism_test():
        x = self.applicative(self.mapper1).ap(self.applicative(self.value))
        y = self.applicative(
            self.mapper1(self.value)
        )
        assert x == y

    def get_interchange_test(self):
        x = self.applicative(self.mapper1)).ap(self.monad(self.value))
        y = self.applicative(lambda fn: fn(self.value).ap(self.applicative(self.mapper1)
        assert x == y

