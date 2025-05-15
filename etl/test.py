import os
import pymupdf

from extraction.batch_splitter import split_into_batches
from extraction.extractor import extract
from transformation.transformer import transform
from load.loader import load


import sqlite3

#get the current working directory
current_directory = os.getcwd()
if __name__ == "__main__":
    
    conn = sqlite3.connect(os.path.join(current_directory, 'data', 'test.db'))
    cursor = conn.cursor()

    # create tables
    # Read SQL queries from an external file
    with open(os.path.join(current_directory, 'others', 'sql', 'table_creation.sql'), 'r') as sql_file:
        sql_script = sql_file.read()

    # Execute the SQL script to create tables
    cursor.executescript(sql_script)

    # Read SQL queries from an external file
    with open(os.path.join(current_directory, 'others', 'sql', 'date_time_table_insertion.sql'), 'r') as sql_file:
        sql_script = sql_file.read()

    # Execute the SQL script to create tables
    cursor.executescript(sql_script)

    cursor.execute("DELETE FROM report_fact;")
    cursor.execute("DELETE FROM contractor_acknowledged_received_by_dim;")
    cursor.execute("DELETE FROM lta_verified_by_dim;")
    cursor.execute("DELETE FROM acknowledgement_dim;")
    cursor.execute("DELETE FROM reported_via_dim;")
    cursor.execute("DELETE FROM inspector_dim;")
    cursor.execute("DELETE FROM supervisor_dim;")
    cursor.execute("DELETE FROM asset_dim;")
    cursor.execute("DELETE FROM location_dim;")
    conn.commit()
    conn.close()

    # split into batches
    report_batches_filenames = split_into_batches(report_folder=os.path.join(current_directory, 'others', 'test_reports_batch'))
    
    for i, report_batch_filenames in enumerate(report_batches_filenames):
        print(f"-----------------------------------------------------------------------------------------\nBatch {i + 1}:")
        report_df = extract(report_batch_filenames=report_batch_filenames)
        report_df = transform(report_batch_dataframe=report_df)
        print(report_df)
        
        report_df.to_csv(os.path.join(current_directory, 'others', 'report_batch_2.csv'), index=False)  
        load(report_df)
        
        print("Batch ETLed")
        
    
    # extraction
    # data = retrieve_input_strings(pdf)
    # data = preprocess_input_strings(data)    
    print("\n Done")
    