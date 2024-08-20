import sys
import os

# Configure directory path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.load import loading
from utils.database import db_connection
from src.transform.transformation import transform_data
from utils.database import db_connection, save_to_mysql
from src.extract import extraction
from tests.data_quality_check import check_data_contract


if __name__ == '__main__':
    # Connect to the database
    db, cursor = db_connection()
    database_name = 'epl_2023/24'
    
    if db and cursor:
        # Data extraction
        column_names = extraction.get_column_names()
        teams = extraction.get_teams()
        extracted_data = extraction.get_data_frame(column_names, teams)
        save_to_mysql(db, cursor, extracted_data)
        
        print('\nExtracted data:')
        print(extracted_data)
        print('')
        
        contract = 'data_extraction_contract.yaml'
        table_name = 'premier_league_table'
        suite_name = 'premier_extraction_league_table_suite'
        success = check_data_contract(contract, database_name, table_name, suite_name)
        print(f"***Data Extraction contract validation {'passed' if success else 'failed'}***")

        # Data transformation and loading
        transformed_data = transform_data(db, cursor)
        
        print('\nTransformed data:')
        print(transformed_data)
        
        loading.load_data(db, cursor, transformed_data)
        contract = 'data_transformation_contract.yaml'
        table_name = 'transformed_premier_league_table'
        suite_name = 'premier_transformation_league_table_suite'
        success = check_data_contract(contract, database_name, table_name, suite_name)
        print(f"***Data Transformation contract validation {'passed' if success else 'failed'}***")