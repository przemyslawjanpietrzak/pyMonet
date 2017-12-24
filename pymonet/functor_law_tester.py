from pymonet.utils import identity


def get_identity_law_test(functor):
    assert functor.map(identity) == functor


def get_composition_law_test(functor, mapper1, mapper2):
    assert functor.map(mapper1).map(mapper2) == functor.map(lambda value: mapper2(mapper1(value)))
