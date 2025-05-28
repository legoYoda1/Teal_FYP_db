import os
import pymupdf
import pandas as pd


def split_into_batches(report_folder : str, batch_size : int) -> list[list[str]]:
    # pdfs loaded from report test batch file
    report_filnames = [os.path.join(report_folder, filename) \
        for filename in os.listdir(report_folder)]
    
    batches = []
    batch = []
    for i, report_filename in enumerate(report_filnames):
        batch.append(report_filename)
        
        if (i + 1) % batch_size == 0 or \
            i + 1 == len(report_filnames):
            batches.append(batch)
            batch = []        
    
    return batches

if __name__ == "__main__":
    print(type(split_into_batches(report_folder=r'.\others\test_reports_batch')))
    pass