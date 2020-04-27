from typing import Dict, Any
from pytest import fixture
from injectark.factory import Factory
from injectark.builder import StrategyBuilder, FactoryBuilder


@fixture
def strategy_builder():
    return StrategyBuilder({
        'base': {
            "QueryParser": {
                "method": "query_parser"
            },
            "TenantProvider": {
                "method": "standard_tenant_provider"
            },
            "OptionRepository": {
                "method": "memory_option_repository"
            }
        },
        'sql': {
            "SqlParser": {
                "method": "sql_query_parser"
            },
            "ConnectionManager": {
                "method": "sql_connection_manager"
            },
            "OptionRepository": {
                "method": "sql_option_repository"
            }
        }
    })


@fixture
def factory_builder():
    class MemoryFactory(Factory):
        def __init__(self, config: Dict[str, Any]) -> None:
            self.config = config

    class SqlFactory(Factory):
        def __init__(self, config: Dict[str, Any]) -> None:
            self.config = config

    class HttpFactory(Factory):
        def __init__(self, config: Dict[str, Any]) -> None:
            self.config = config

    return FactoryBuilder([MemoryFactory, SqlFactory, HttpFactory])


def test_strategy_builder(strategy_builder):
    strategy = strategy_builder.build(['base', 'sql'])
    assert strategy == {
        "QueryParser": {
            "method": "query_parser"
        },
        "TenantProvider": {
            "method": "standard_tenant_provider"
        },
        "SqlParser": {
            "method": "sql_query_parser"
        },
        "ConnectionManager": {
            "method": "sql_connection_manager"
        },
        "OptionRepository": {
            "method": "sql_option_repository"
        }
    }


def test_strategy_builder_custom_strategy(strategy_builder):
    strategy = strategy_builder.build(['base'], custom_strategy={
        "OptionRepository": {
            "method": "object_storage_option_repository"
        }
    })
    assert strategy == {
        "QueryParser": {
            "method": "query_parser"
        },
        "TenantProvider": {
            "method": "standard_tenant_provider"
        },
        "OptionRepository": {
            "method": "object_storage_option_repository"
        }
    }


def test_factory_builder(factory_builder):
    factory = factory_builder.build({'factory': 'MemoryFactory'})
    assert type(factory).__name__ == 'MemoryFactory'

    factory = factory_builder.build({'factory': 'SqlFactory'})
    assert type(factory).__name__ == 'SqlFactory'

    factory = factory_builder.build({'key': 'value'}, name='HttpFactory')
    assert type(factory).__name__ == 'HttpFactory'
    factory.config == {'key': 'value'}

    factory = factory_builder.build(
        {'factory': 'MemoryFactory', 'key': 'value'}, name='HttpFactory')
    assert type(factory).__name__ == 'HttpFactory'
    factory.config == {'key': 'value'}
