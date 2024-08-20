import os
import sys
import yaml
from great_expectations.data_context import BaseDataContext
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.core.batch import BatchRequest

# Configure path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from configurations.config import project_config

def check_data_contract(contract: str, database_name: str, table_name: str, suite: str) -> object:
    # Get script's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the contract file
    contract_path = os.path.join(current_dir, f'contracts/{contract}')
     
    # Read the YAML file
    with open(contract_path, 'r') as file:
        data_contract = yaml.safe_load(file)
    
    # Initialize the DataContext
    context = BaseDataContext(project_config=project_config)

    # Create or get the expectation suite
    suite_name = suite

    try:
        expectation_suite = context.get_expectation_suite(suite_name)
    except:
        expectation_suite = ExpectationSuite(expectation_suite_name=suite_name)
        context.add_or_update_expectation_suite(expectation_suite=expectation_suite)

    # Create a BatchRequest object
    batch_request = BatchRequest(
        datasource_name='premier_league',
        data_connector_name='default_inferred_data_connector_name',
        data_asset_name=f'{database_name}.{table_name}'
    )

    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=data_contract['expectation_suite_name']
    )

    for expectation in data_contract['expectations']:
        expectation_type = expectation['expectation_type']
        kwargs = expectation['kwargs']
        
        if expectation_type == 'expect_query_result_to_be_in_range':
            validator.expect_query_result_to_be_in_range(**kwargs)
        else:
            getattr(validator, expectation_type)(**kwargs)

    # Save the expectation suite
    context.save_expectation_suite(validator.expectation_suite)

    # Run the validation
    results = validator.validate()
    print(results)
    
    return results.success