from pymonet.box import Box
from pymonet.either import Left, Right
from pymonet.maybe import Maybe


class TransformMonadTester:

    def __init__(self, monad, value, is_fail=False):
        self.monad = monad
        self.value = value
        self.is_fail = is_fail

    def to_box_test(self):
        assert self.monad(self.value).to_box() == Box(self.value)

    def to_maybe_test(self):
        assert self.monad(self.value).to_maybe() == Maybe.just(self.value) if not self.is_fail else Maybe.nothing()

    def to_either_test(self):
        assert self.monad(self.value).to_maybe() == Right(self.value) if not self.is_fail else Left(self.value)

    def test(self, run_to_box_test, run_to_maybe_test, run_to_either_test):
        if run_to_box_test:
            self.to_box_test()
        if run_to_maybe_test:
            self.to_maybe_test()
        if run_to_either_test:
            self.to_either_test()
