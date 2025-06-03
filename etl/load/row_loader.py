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

def load_report_batch_row(report_batch_row : pd.Series, cursor : sqlite3.Cursor, conn : None):

    print("Attempting to load row")
    try:
        load_dim_non_repeatable_field(report_batch_row['Supervised_by'], 'supervisor_dim', 'name', foreign_key_id, cursor, conn)
        load_dim_non_repeatable_field(report_batch_row['Inspected_by'], 'inspector_dim', 'name', foreign_key_id, cursor, conn)
        
        try:
            cursor.execute(f'''
                SELECT asset_id
                    FROM asset_dim
                    WHERE asset_type = '{report_batch_row['Type_of_asset']}'
            ''')

            print(report_batch_row['Type_of_asset'])
            row_id = (cursor.fetchone())[0]
            
            foreign_key_id['asset_dim'] = row_id
            # print(row_id)
            
            conn.commit()
        except KeyError as e:
            print("DB error: ", e)
            
        try:
            print(report_batch_row['Location'], report_batch_row['Landmark'])
            cursor.execute(f'''
                SELECT location_id
                    FROM location_dim
                    WHERE location = '{report_batch_row['Location']}' and lamppost_id = '{report_batch_row['Landmark']}'
            ''')
            foo = cursor.fetchone()
            
            if foo == None:
                foreign_key_id['location_dim'] = 'C001A'    
            else:
                row_id = foo[0]
                foreign_key_id['location_dim'] = row_id
            
            conn.commit()
        except KeyError as e:
            print("DB error: ", e)

        # load_dim(dim='reported_via_dim', fields=('method', 'agency', 'date_id', 'time_id'), 
        #          values=(report_batch_row['Reported_via__method'], report_batch_row['Reported_via__agency'], 
        #                  report_batch_row['Reported_via__date'], report_batch_row['Reported_via__time']),
        #          foreign_key_id=foreign_key_id, 
        #          cursor=cursor, conn=conn
        #          )
        # load_dim(dim='acknowledgement_dim', fields=('method', 'date_id', 'time_id'), 
        #          values=(report_batch_row['Reported_via__method'], report_batch_row['Reported_via__date'], 
        #                  report_batch_row['Reported_via__time']),
        #          foreign_key_id=foreign_key_id, 
        #          cursor=cursor, conn=conn
        #          )


        # Inserting data into report_fact table
        cursor.execute('''
            INSERT INTO report_fact (defect_ref_no, date_id, location_id, asset_id, supervisor_id, inspector_id, 
            repeated_defect, description, quantity, measurement, cause_of_defect, recommendation, report_path) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            report_batch_row['Defect_ref_no'], 
            report_batch_row['Date'], 
            foreign_key_id['location_dim'], 
            foreign_key_id['asset_dim'], 
            foreign_key_id['supervisor_dim'], 
            foreign_key_id['inspector_dim'], 
            # foreign_key_id['reported_via_dim'], 
            # foreign_key_id['acknowledgement_dim'],
            report_batch_row['Repeated_defect'], 
            report_batch_row['Description'], 
            report_batch_row['Quantity'], 
            report_batch_row['Measurement'], 
            report_batch_row['Cause_of_defect'], 
            report_batch_row['Recommendation'],
            report_batch_row['Report_path'],
        )) 
        
        conn.commit()
    except KeyError as e:
        print('Db error: ', e)
        raise