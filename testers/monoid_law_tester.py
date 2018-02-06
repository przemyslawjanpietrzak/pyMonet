class MonoidLawTester:

    def __init__(self, monoid, value):
        self.monoid = monoid
        self.value = value

    def left_identity_test(self):
        monoid = self.monoid(self.value)
        assert monoid.concat(monoid.neutral()) == monoid

    def right_identity_test(self):
        monoid = self.monoid(self.value)
        assert monoid.neutral().concat(monoid) == monoid

    def test(self):
        self.left_identity_test()
        self.right_identity_test()
