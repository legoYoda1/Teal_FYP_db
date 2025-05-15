import os
import pymupdf

from extraction.batch_splitter import split_into_batches
from extraction.extractor import extract
from transformation.transformer import transform
from load.loader import load, clear_db


import sqlite3


#get the current working directory
current_directory = os.getcwd()
if __name__ == "__main__":

    # clear_db()
    
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
        
    print("\n Done")
    