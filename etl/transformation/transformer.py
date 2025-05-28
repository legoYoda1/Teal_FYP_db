from datetime import datetime
import pandas as pd

from etl.transformation.row_transformer import preprocess_report_batch_row

def transform(report_batch_dataframe : pd.DataFrame) -> pd.DataFrame:
    report_batch_dataframe = report_batch_dataframe.apply(preprocess_report_batch_row, axis=1)
    return report_batch_dataframe

if __name__ == '__main__':
    # test_df = pd.read_csv(r'C:\Projects\PDF_Text_Extraction\others\report_batch.csv')
    # test_df = transform(test_df)
    # test_df.to_csv(r'C:\Projects\PDF_Text_Extraction\others\report_batch_2.csv')
    # print('bruh')
    pass
