from injectark import Factory


def test_factory_extract() -> None:
    class MockFactory(Factory):
        def __init__(self, context):
            pass

        def _my_method(self):
            pass

    factory = MockFactory({})
    method = factory.extract('_my_method')

    assert method == factory._my_method
