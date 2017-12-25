from pymonet.box import Box
from pymonet.either import Left, Right
from pymonet.maybe import Maybe
from pymonet.monad_try import Try
from pymonet.validation import Validation
from pymonet.utils import identity


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
        assert self.monad(self.value).to_either() == Right(self.value) if not self.is_fail else Left(self.value)

    def to_lazy_test(self):
        assert self.monad(self.value).to_lazy().fold(identity) == self.value

    def to_try_test(self):
        assert self.monad(self.value).to_try() == Try(self.value, is_success=not self.is_fail)

    def to_validation_test(self):
        assert (
            self.monad(self.value).to_validation()
            ==
            Validation.success(self.value) if not self.is_fail else Validation.fail(self.value)
        )

    def test(
        self,
        run_to_box_test=True,
        run_to_maybe_test=True,
        run_to_either_test=True,
        run_to_lazy_test=True,
        run_to_try_test=True,
        run_to_validation_test=True
    ):
        if run_to_box_test:
            self.to_box_test()
        if run_to_maybe_test:
            self.to_maybe_test()
        if run_to_either_test:
            self.to_either_test()
        if run_to_lazy_test:
            self.to_lazy_test()
        if run_to_try_test:
            self.to_try_test()
        if run_to_validation_test:
            self.to_validation_test()
