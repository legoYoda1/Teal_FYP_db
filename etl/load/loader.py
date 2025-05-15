import sqlite3
import pandas as pd
from load.row_loader import load_report_batch_row

def load(report_batch_dataframe : pd.DataFrame) -> None:
    
    conn = sqlite3.connect(r'C:\Projects\DB_report_test2\test.db')
    cursor = conn.cursor()
    
    report_batch_dataframe = report_batch_dataframe.apply(lambda row: load_report_batch_row(row, cursor=cursor, conn=conn), axis=1)
    conn.close()
    pass

def clear_db() -> None:
    conn = sqlite3.connect(r'C:\Projects\DB_report_test2\test.db')
    cursor = conn.cursor()
    
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
