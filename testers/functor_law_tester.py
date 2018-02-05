from pymonet.utils import identity


class FunctorLawTester:  # pragma: no cover

    def __init__(self, functor, mapper1, mapper2, get_fn=identity):
        self.functor = functor
        self.mapper1 = mapper1
        self.mapper2 = mapper2
        self.get_fn = get_fn

    def _assert(self, x, y):
        assert self.get_fn(x) == self.get_fn(y)

    def identity_law_test(self):
        x = self.functor.map(identity)
        y = self.functor

        self._assert(x, y)

    def composition_law_test(self):
        mapped_functor1 = self.functor.map(self.mapper1).map(self.mapper2)
        mapped_fuctor2 = self.functor.map(lambda value: self.mapper2(self.mapper1(value)))
        self._assert(mapped_functor1, mapped_fuctor2)

    def test(self, run_identity_law_test=True, run_composition_law_test=True):
        if run_identity_law_test:
            self.identity_law_test()
        if run_composition_law_test:
            self.composition_law_test()
