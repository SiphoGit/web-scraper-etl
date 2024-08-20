import pandas as pd

def transform_data(db:object, cursor:object) -> pd.DataFrame:
    try:
        # Fetch all data from the table
        table_name = 'premier_league_table'
        query = f'SELECT * FROM {table_name}'
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Get column names
        column_names = [desc[0] for desc in cursor.description]

        # Create a pandas DataFrame
        df = pd.DataFrame(rows, columns=column_names)

        # Rename columns
        new_column_names = {
            'No': 'position',
            'Teams': 'team_name',
            'GP': 'games_played',
            'W': 'won',
            'D': 'drawn',
            'L': 'lost',
            'GF': 'goals_scored',
            'GA': 'goals_conceded',
            'GD': 'goal_difference',
            'PTS': 'points'
        }

        df = df.rename(columns=new_column_names)   

        # Save the DataFrame to a CSV file
        df.to_csv('data/premier_league_table.csv', index=False)
        return df
    except Exception as e:
        print(f'Error: {e}')
        db.rollback()
        db.close()
        cursor.close()