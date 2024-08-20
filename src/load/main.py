import sys
import os
import loading

# Configure directory path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.database import db_connection
from src.transform.transformation import transform_data
from tests.data_quality_check import check_data_contract


if __name__ == '__main__':
    db, cursor = db_connection()
    # Data transformation and loading
    transformed_data = transform_data(db, cursor)
    
    print('\nTransformed data:')
    print(transformed_data)
    
    loading.load_data(db, cursor, transformed_data)
    
    database_name = 'epl_2023/24'  
    contract = 'data_transformation_contract.yaml'
    table_name = 'transformed_premier_league_table'
    suite_name = 'premier_transformation_league_table_suite'
    success = check_data_contract(contract, database_name, table_name, suite_name)
    print(f"***Data Transformation contract validation {'passed' if success else 'failed'}***")