from .conftest import A, B, C, D, X, Y


def test_resolver_instantiation(resolver):
    assert resolver is not None


def test_resolver_attributes(resolver, standard_strategy, standard_factory):
    assert resolver.parent is None
    assert resolver.strategy == standard_strategy
    assert resolver.factory == standard_factory
    assert resolver.registry == {}


def test_resolver_resolves_resource_without_dependencies(resolver):
    instance = resolver.resolve('A')
    assert isinstance(instance, A)
    instance = resolver.resolve('B')
    assert isinstance(instance, B)
    assert len(resolver.registry) == 2


def test_resolver_serves_resources_from_registry(resolver):
    instance = resolver.resolve('A')
    assert isinstance(instance, A)
    registry_instance = resolver.resolve('A')
    assert instance == registry_instance
    assert len(resolver.registry) == 1


def test_resolver_resolves_resource_with_dependencies(resolver):
    instance = resolver.resolve('C')
    assert isinstance(instance, C)
    assert isinstance(instance.a, A)
    assert isinstance(instance.b, B)
    assert resolver.resolve('A') == instance.a
    assert resolver.resolve('B') == instance.b


def test_resolver_doesnt_persist_ephemeral_dependencies(resolver):
    resolver.strategy = {
        'A': {
            'method': 'standard_a',
            'ephemeral': True
        }
    }
    instance = resolver.resolve('A')
    assert isinstance(instance, A)
    assert len(resolver.registry) == 0


def test_resolver_forge(resolver, standard_strategy, standard_factory):
    parent = resolver

    resolver = parent.forge(
        strategy=standard_strategy, factory=standard_factory)

    assert resolver is not None
    assert resolver.parent is parent


def test_resolver_resolves_a_resource_owned_by_its_parent(
        resolver, parent_resolver):
    parent_resolver.registry['X'] = X()
    resolver.parent = parent_resolver

    instance = resolver.resolve('X')
    assert isinstance(instance, X)

    assert instance == resolver.parent.registry['X']
    assert len(resolver.parent.registry) == 1
    assert len(resolver.registry) == 0


def test_resolver_resolve_a_resource_its_parent_know(
        resolver, parent_resolver):
    resolver.parent = parent_resolver

    instance = resolver.resolve('Y')
    assert isinstance(instance, Y)
    assert instance == resolver.parent.registry['Y']
    # assert instance == resolver.registry['Y']
    assert len(resolver.parent.registry) == 2
    assert len(resolver.registry) == 0


def test_resolver_registry_fetch_unique(resolver):
    resolver.strategy = {
        'B': {
            'method': 'standard_b',
            'unique': True
        }
    }
    result = resolver._registry_fetch('B')
    assert result is False
