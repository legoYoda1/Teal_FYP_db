import sqlite3
import pandas as pd
from load.row_loader import load_report_batch_row

def load(report_batch_dataframe : pd.DataFrame) -> None:
    
    conn = sqlite3.connect(r'.\data\test.db')
    cursor = conn.cursor()
    
    report_batch_dataframe = report_batch_dataframe.apply(lambda row: load_report_batch_row(row, cursor=cursor, conn=conn), axis=1)
    conn.close()
    pass
