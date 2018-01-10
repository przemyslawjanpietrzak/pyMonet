from pymonet.utils import identity


class MonadLawTester:  # pragma: no cover

    def __init__(self, monad, value, mapper1, mapper2, get_fn=identity):
        self.monad = monad
        self.value = value
        self.mapper1 = mapper1
        self.mapper2 = mapper2
        self.get_fn = get_fn

    def _assert(self, x, y):
        assert self.get_fn(x) == self.get_fn(y)

    def associativity_test(self):
        x = self.monad(self.value).bind(self.mapper1).bind(self.mapper2)
        y = self.monad(self.value).bind(lambda value: self.mapper2(value).bind(self.mapper1))

        self._assert(x, y)

    def left_unit_test(self):
        self._assert(self.monad(self.value).bind(self.mapper1), self.mapper1(self.value))

    def right_unit_test(self):
        self._assert(self.monad(self.value).bind(lambda value: self.monad(value)), self.monad(self.value))

    def test(self, run_associativity_law_test=True, run_left_law_test=True, run_right_law_test=True):
        if run_associativity_law_test:
            self.associativity_test()
        if run_left_law_test:
            self.left_unit_test()
        if run_right_law_test:
            self.right_unit_test()
