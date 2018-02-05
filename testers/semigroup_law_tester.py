class SemigroupLawTester:

    def __init__(self, semigroup, value1, value2, value3):
        self.semigroup = semigroup
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3

    def associativity_test(self):

        x = self.semigroup(self.value1)\
                .concat(self.semigroup(self.value2))\
                .concat(self.semigroup(self.value3))

        y = self.semigroup(self.value1).concat(
                self.semigroup(self.value2).self.semigroup(self.value3)
            )

        assert x == y

    def test(self):
        self.associativity_test()
