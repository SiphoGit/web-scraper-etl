import os
from great_expectations.data_context.types.base import DataContextConfig
from dotenv import dotenv_values


# Database configuration
config = dotenv_values('.env')
password = config.get('password')
user_name = config.get('user')
database = config.get('database')

# Path configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
tests_results_dir = os.path.join(current_dir, '../tests/tests_results')
    
# Create the project configuration
project_config = DataContextConfig(
    config_version=3.0,
    datasources={
        'premier_league': {
            'execution_engine': {
                'module_name': 'great_expectations.execution_engine',
                'class_name': 'SqlAlchemyExecutionEngine',
                'connection_string': f'mysql+pymysql://{user_name}:{password}@127.0.0.1:3306/{database}'
            },
            'data_connectors': {
                'default_inferred_data_connector_name': {
                    'class_name': 'InferredAssetSqlDataConnector',
                    'include_schema_name': True
                }
            }
        }
    },
    stores={
        'expectations_store': {
            'class_name': 'ExpectationsStore',
            'store_backend': {
                'class_name': 'TupleFilesystemStoreBackend',
                'base_directory': os.path.join(tests_results_dir, 'expectations')
            }
        },
        'validations_store': {
            'class_name': 'ValidationsStore',
            'store_backend': {
                'class_name': 'TupleFilesystemStoreBackend',
                'base_directory': os.path.join(tests_results_dir, 'validations')
            }
        },
        'evaluation_parameter_store': {'class_name': 'EvaluationParameterStore'}
    },
    expectations_store_name='expectations_store',
    validations_store_name='validations_store',
    evaluation_parameter_store_name='evaluation_parameter_store',
    data_docs_sites={
        'local_site': {
            'class_name': 'SiteBuilder',
            'show_how_to_buttons': True,
            'store_backend': {
                'class_name': 'TupleFilesystemStoreBackend',
                'base_directory': os.path.join(tests_results_dir, 'data_docs')
            }
        }
    }
)