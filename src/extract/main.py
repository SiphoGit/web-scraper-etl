import sys
import os

# Configure the root directory path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from utils.database import db_connection, save_to_mysql
import extraction 
from tests.data_quality_check import check_data_contract

if __name__ == '__main__':
        # Data extraction
        column_names = extraction.get_column_names()
        teams = extraction.get_teams()
        extracted_data = extraction.get_data_frame(column_names, teams)
        db, cursor = db_connection()
        save_to_mysql(db, cursor, extracted_data)
        
        print('\nExtracted data:')
        print(extracted_data)
        print('')
        
        database_name = 'epl_2023/24'
        contract = 'data_extraction_contract.yaml'
        table_name = 'premier_league_table'
        suite_name = 'premier_extraction_league_table_suite'
        success = check_data_contract(contract, database_name, table_name, suite_name)
        print(f"***Data Extraction contract validation {'passed' if success else 'failed'}***")