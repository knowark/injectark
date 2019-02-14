from pytest import fixture
from injectark.injectark import Injectark


class A:
    pass


class B:
    pass


class C:
    def __init__(self, a: A, b: B) -> None:
        self.a = a
        self.b = b


class D:
    def __init__(self, b: B, c: C) -> None:
        self.b = b
        self.c = c


@fixture
def standard_factory():
    class StandardFactory:
        def extract(self, method: str):
            return getattr(self, "_{0}".format(method), None)

        def _standard_a(self):
            return A()

        def _standard_b(self):
            return B()

        def _standard_c(self, a: A, b: B):
            return C(a, b)

        def _standard_d(self, b: B, c: C):
            return D(b, c)

    return StandardFactory()


@fixture
def standard_strategy():
    return {
        'A': {
            'method': 'standard_a'
        },
        'B': {
            'method': 'standard_b'
        },
        'C': {
            'method': 'standard_c'
        },
        'D': {
            'method': 'standard_d'
        }
    }


class X:
    pass


class Y:
    def __init__(self, x: X) -> None:
        self.x = x


@fixture
def core_factory():
    class CoreFactory:
        def extract(self, method: str):
            return getattr(self, "_{0}".format(method))

        def _core_x(self):
            return X()

        def _core_y(self, x: X):
            return Y(x)

    return CoreFactory()


@fixture
def core_strategy():
    return {
        'X': {
            'method': 'core_x'
        },
        'Y': {
            'method': 'core_y'
        }
    }


@fixture
def resolver(standard_strategy, standard_factory):
    return Injectark(strategy=standard_strategy, factory=standard_factory)


@fixture
def parent_resolver(core_strategy, core_factory):
    return Injectark(strategy=core_strategy, factory=core_factory)
