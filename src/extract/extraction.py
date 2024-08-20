import pandas as pd
import sys
import os

# Configure the root directory path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from utils.page_request import request_page


soup = request_page()

def get_column_names() -> list[str]:
    try:
        print(f'Scraping column names...')
        
        column_names_element = soup.find('thead', class_='Epl2Pt_thd')
        column_names = [column.text.strip().split('\n') for column in column_names_element]
        column_names = column_names[1]
        
        return column_names
    except Exception as e:
        print(f'Error: {e}')
        
def get_teams() -> list[list]:
    try:
        print(f'Scraping PSL 2023/24 table...')

        # Get the table body
        table_element = soup.find('tbody', class_='Epl2Pt_tbdy')
        
        # Find all rows
        rows = table_element.find_all('tr', class_='Epl2Pt_tr')
        
        data = []
        for row in rows:
            # Find all cells in the row
            cells = row.find_all('td', class_='Epl2Pt_td')
            
            row_data = []
            for cell in cells:
                # Exclude the content from 'tip_wrp' class
                if cell.find(class_='tip_wrp'):
                    cell.find(class_='tip_wrp').extract()
                
                cell_text = cell.get_text(strip=True)
                
                # For cells with multiple team names, take the first one
                if cell.find_all('a', class_='Epl2Pt_txt'):
                    cell_text = cell.find('a', class_='Epl2Pt_txt').get_text(strip=True)
                
                row_data.append(cell_text)
            
            if not row_data[0].startswith('Recent Results'):
                data.append(row_data[:-1])
        print(f'Successfully extracted data!\n')
        
        return data
    except Exception as e:
        print(f'Error: {e}')

def get_data_frame(column_names: list[str], data: list[list]) -> pd.DataFrame:
    df = pd.DataFrame(data, columns=column_names)
    
    # Convert numeric columns to appropriate data types
    numeric_columns = ['No', 'GP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'PTS']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

    return df