import random
import sqlite3

import pandas as pd

foreign_key_id = {
}

def load_dim(dim : str, fields : tuple, values: tuple, foreign_key_id : dict, cursor : sqlite3.Cursor, conn : None) -> None:
    try:
        fields_string = ', '.join(fields)
        values_placeholder_string = ', '.join(['?'] * len(fields))
        
        cursor.execute(f'''
            INSERT INTO {dim} ({fields_string})
            VALUES ({values_placeholder_string})
        ''', values)

        row_id = cursor.lastrowid
        foreign_key_id[dim] = row_id
                    
        conn.commit()
    except KeyError as e:
        print("DB error: ", e)
        raise
            

def load_dim_non_repeatable_field(value : any, dim : str, field : str, foreign_key_id : dict, cursor : sqlite3.Cursor, conn : None) -> None:
    try:
            cursor.execute(f'''
                WITH row_id AS (
                    SELECT rowid
                    FROM {dim}
                    WHERE {field} = ?
                    LIMIT 1
                )
                INSERT INTO {dim} ({field})
                SELECT ?
                WHERE NOT EXISTS (SELECT 1 FROM row_id);
            ''', (value, value,))
            cursor.execute(f'''
                SELECT rowid FROM {dim} WHERE {field} = ?;
            ''', (value,))

            row_id = (cursor.fetchone())[0]
            foreign_key_id[dim] = row_id
            # print(row_id)
            
            conn.commit()
    except KeyError as e:
        print("DB error: ", e)

# NOTICE these are dummy data for testing!!!
# Subject to change in the future
location_ids = [
    'or1A', 'or1B', 'or1C', 'or1D', 'or1E', 'or1F', 
    'or2A', 'or2B', 'or2C', 'or2D', 'or2E', 'or2F',
    'mp1A', 'mp1B', 'mp1C', 'mp1D', 'mp1E', 'mp1F',
    'mp2A', 'mp2B', 'mp2C', 'mp2D', 'mp2E', 'mp2F',
    'rp1A', 'rp1B', 'rp1C', 'rp1D', 'rp1E', 'rp1F',
    'rp2A', 'rp2B', 'rp2C', 'rp2D', 'rp2E', 'rp2F',
    'ecp1A', 'ecp1B', 'ecp1C', 'ecp1D', 'ecp1E', 'ecp1F',
    'ecp2A', 'ecp2B', 'ecp2C', 'ecp2D', 'ecp2E', 'ecp2F',
    'st1A', 'st1B', 'st1C', 'st1D', 'st1E', 'st1F',
    'st2A', 'st2B', 'st2C', 'st2D', 'st2E', 'st2F'
]

asset_ids = [
    'crk', 'pth', 'def', 'sfd', 'jnt', 'drn',
    'shd', 'wcr', 'utd', 'str'
]
  

def load_report_batch_row(report_batch_row : pd.Series, cursor : sqlite3.Cursor, conn : None):

    print("Attempting to load row")
    try:
        load_dim_non_repeatable_field(report_batch_row['supervised_by'], 'supervisor_dim', 'name', foreign_key_id, cursor, conn)
        load_dim_non_repeatable_field(report_batch_row['inspected_by'], 'inspector_dim', 'name', foreign_key_id, cursor, conn)

        # Inserting data into report_fact table
        cursor.execute('''
            INSERT INTO report_fact (defect_ref_no, date_id, location_id, asset_id, supervisor_id, inspector_id,  
            repeated_defect, description, quantity, measurement, cause_of_defect, recommendation) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            report_batch_row['defect_ref_no'], 
            report_batch_row['date'], 
            location_ids[random.randint(0, len(location_ids)-1)], 
            asset_ids[random.randint(0, len(asset_ids)-1)], 
            foreign_key_id['supervisor_dim'], 
            foreign_key_id['inspector_dim'],
            report_batch_row['repeated_defect'], 
            report_batch_row['description'], 
            report_batch_row['quantity'], 
            report_batch_row['measurement'], 
            report_batch_row['cause_of_defect'], 
            report_batch_row['recommendation']
        )) 
        
        conn.commit()
    except KeyError as e:
        print('Db error: ', e)
        raise