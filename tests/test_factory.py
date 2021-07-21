from injectark import Factory


def test_factory_extract() -> None:
    class MockFactory(Factory):
        def __init__(self, config):
            super().__init__(config)
            pass

        def _my_method(self):
            pass

    factory = MockFactory({'key': 'value'})
    method = factory.extract('_my_method')

    assert method == factory._my_method
    assert factory.config == {'key': 'value'}
