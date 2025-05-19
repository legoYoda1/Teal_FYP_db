import sqlite3
import pandas as pd

foreign_key_id = {
    # 'supervisor_dim' : None
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
            

def load_report_batch_row(report_batch_row : pd.Series, cursor : sqlite3.Cursor, conn : None):

    print("bruh")
    try:
        load_dim_non_repeatable_field(report_batch_row['Supervised_by'], 'supervisor_dim', 'name', foreign_key_id, cursor, conn)
        load_dim_non_repeatable_field(report_batch_row['Inspected_by'], 'inspector_dim', 'name', foreign_key_id, cursor, conn)

        load_dim(dim='reported_via_dim', fields=('method', 'agency', 'date_id', 'time_id'), 
                 values=(report_batch_row['Reported_via__method'], report_batch_row['Reported_via__agency'], 
                         report_batch_row['Reported_via__date'], report_batch_row['Reported_via__time']),
                 foreign_key_id=foreign_key_id, 
                 cursor=cursor, conn=conn
                 )
        load_dim(dim='acknowledgement_dim', fields=('method', 'date_id', 'time_id'), 
                 values=(report_batch_row['Reported_via__method'], report_batch_row['Reported_via__date'], 
                         report_batch_row['Reported_via__time']),
                 foreign_key_id=foreign_key_id, 
                 cursor=cursor, conn=conn
                 )
        load_dim(dim='lta_verified_by_dim', fields=('name', 'date_id', 'instructions', 'wso_no'), 
                 values=(report_batch_row['Defects_verified_by__name'], report_batch_row['Defects_verified_by__date'], 
                         report_batch_row['Instructions'], report_batch_row['WSO_no']),
                 foreign_key_id=foreign_key_id, 
                 cursor=cursor, conn=conn
                 )
        load_dim(dim='contractor_acknowledged_received_by_dim', fields=('name', 'date_id'), 
                 values=(report_batch_row['Acknowledged_and_received_by__name'], 
                         report_batch_row['Acknowledged_and_received_by__date']),
                 foreign_key_id=foreign_key_id, 
                 cursor=cursor, conn=conn
                 )

        # Inserting data into report_fact table
        cursor.execute('''
            INSERT INTO report_fact (defect_ref_no, date_id, location_id, asset_id, supervisor_id, inspector_id, 
            reported_via_id, acknowledgement_id, lta_verified_by_id, contractor_acknowledged_received_by_id, 
            repeated_defect, description, quantity, measurement, cause_of_defect, reccomendation) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            report_batch_row['Defect_ref_no'], 
            report_batch_row['Date'], 
            '1', 
            '1', 
            foreign_key_id['supervisor_dim'], 
            foreign_key_id['inspector_dim'], 
            foreign_key_id['reported_via_dim'], 
            foreign_key_id['acknowledgement_dim'], 
            foreign_key_id['lta_verified_by_dim'], 
            foreign_key_id['contractor_acknowledged_received_by_dim'], 
            report_batch_row['Repeated_defect'], 
            report_batch_row['Description'], 
            report_batch_row['Quantity'], 
            report_batch_row['Measurement'], 
            report_batch_row['Cause_of_defect'], 
            report_batch_row['Recommendation']
        ))  # Replace with actual values
        conn.commit()

        # cursor.execute('''
        #     SELECT * FROM report_fact;
        # ''')
        # print(cursor.fetchall())
    # pass
    except KeyError as e:
        print('Db error: ', e)
        raise