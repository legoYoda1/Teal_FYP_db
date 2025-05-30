import os
import sqlite3
import time

import pandas as pd
import pymupdf

if __name__ != "__main__":
    from etl.extraction.batch_splitter import split_into_batches
    from etl.extraction.extractor import extract
    from etl.load.loader import clear_db, load
    from etl.transformation.transformer import transform
else:
    from extraction.batch_splitter import split_into_batches
    from extraction.extractor import extract
    from load.loader import clear_db, load
    from transformation.transformer import transform



if __name__ == "__main__":

    clear_db()
    
    # split into batches
    report_batches_filenames = split_into_batches(report_folder=os.path.join('.', 'others', 'test_reports_batch'))
    
    for i, report_batch_filenames in enumerate(report_batches_filenames):
        print(f"-----------------------------------------------------------------------------------------\nBatch {i + 1}:")
        report_df = extract(report_batch_filenames=report_batch_filenames)
        report_df = transform(report_batch_dataframe=report_df)
        print(report_df)
        
        # for debuggine
        report_df.to_csv(os.path.join('.', 'others', 'misc', 'report_batch_2.csv'), index=False)  
        load(report_df)
        
        print("Batch ETLed")
        
    print("\n Done")
    
def etl(report_folder, batch_size = 0, socketio = None):
    
    if batch_size == 0:
        batch_size = 2  # default batch size
        
    clear_db()
    
    # split into batches
    # report_batches_filenames = split_into_batches(report_folder=os.path.join('.', 'others', 'test_reports_batch'))
    report_batches_filenames = split_into_batches(report_folder, batch_size)
    
    
    for i, report_batch_filenames in enumerate(report_batches_filenames):
        if socketio:
            socketio.emit('batch_upload_status_update', {'batch_no': i + 1, 'total_batches': len(report_batches_filenames)})

        # print("BATCH NO", batch_upload_status['batch_no'])
        print(f"-----------------------------------------------------------------------------------------\nBatch {i + 1}:")
        report_df = extract(report_batch_filenames=report_batch_filenames)
        report_df = transform(report_batch_dataframe=report_df)
        # print(report_df)
        
        # for debuggine
        report_df.to_csv(os.path.join('.', 'others', 'misc', 'report_batch_2.csv'), index=False)
        load(report_df)
        
        print("Batch ETLed")
        
    print("\n Done")

def bruh():
    print("bruh")