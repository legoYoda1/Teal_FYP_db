import sqlite3
import pandas as pd

def load_report_batch_row(report_batch_row : pd.Series, cursor : sqlite3.Cursor, conn : None):
# def load_report_batch_row(report_batch_row : pd.Series):

    try:
        # print(report_batch_row)
        # Inserting data into supervisor_dim table
        cursor.execute('''
            INSERT INTO supervisor_dim (name) 
            VALUES (?)
        ''', (report_batch_row['Supervised_by'],))  # Replace with actual name
        conn.commit()
        

        # Inserting data into inspector_dim table
        cursor.execute('''
            INSERT INTO inspector_dim (name) 
            VALUES (?)
        ''', (report_batch_row['Inspected_by'],))  # Replace with actual name
        conn.commit()

        # Inserting data into reported_via_dim table
        cursor.execute('''
            INSERT INTO reported_via_dim (method, agency, date_id, time_id) 
            VALUES (?, ?, ?, ?)
        ''', (report_batch_row['Reported_via__method'], report_batch_row['Reported_via__agency'], report_batch_row['Reported_via__date'], report_batch_row['Reported_via__time']))  # Replace with actual date_id and time_id
        conn.commit()

        # Inserting data into acknowledgement_dim table
        cursor.execute('''
            INSERT INTO acknowledgement_dim (method, date_id, time_id) 
            VALUES (?, ?, ?)
        ''', (report_batch_row['Reported_via__method'], report_batch_row['Reported_via__date'], report_batch_row['Reported_via__time']))
        conn.commit()

        # Inserting data into lta_verified_by_dim table
        cursor.execute('''
            INSERT INTO lta_verified_by_dim (name, date_id, instructions, wso_no) 
            VALUES (?, ?, ?, ?)
        ''', (report_batch_row['Defects_verified_by__name'], report_batch_row['Defects_verified_by__date'], report_batch_row['Instructions'], report_batch_row['WSO_no']))  # Replace with actual values
        conn.commit()

        # Inserting data into contractor_acknowledged_received_by_dim table
        cursor.execute('''
            INSERT INTO contractor_acknowledged_received_by_dim (name, date_id) 
            VALUES (?, ?)
        ''', (report_batch_row['Acknowledged_and_received_by__name'], report_batch_row['Acknowledged_and_received_by__date']))  # Replace with actual date_id
        conn.commit()

        # Inserting data into report_dim table
        cursor.execute('''
            INSERT INTO report_fact (defect_ref_no, date_id, location_id, asset_id, supervisor_id, inspector_id, 
            reported_via_id, acknowledgement_id, lta_verified_by_id, contractor_acknowledged_received_by_id, 
            repeated_defect, description, quantity, measurement, cause_of_defect, reccomendation) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            report_batch_row['Defect_ref_no'], report_batch_row['Date'], '1', '1', 
            1, 1, 1, 1, 
            1, 1, report_batch_row['Repeated_defect'], 
            report_batch_row['Description'], report_batch_row['Quantity'], report_batch_row['Measurement'], 
            report_batch_row['Cause_of_defect'], report_batch_row['Recommendation']
        ))  # Replace with actual values
        
        conn.commit()

        # cursor.execute('''
        #     SELECT * FROM report_fact;
        # ''')
        # print(cursor.fetchall())
    # pass
    except KeyError as e:
        print('Db error: ', e)