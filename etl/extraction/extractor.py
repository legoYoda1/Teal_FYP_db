import os
import pymupdf
import pandas as pd

if __name__ != "__main__":
    from etl.transformation.db_input import db_input_fields
    from etl.extraction.text_extractor import retrieve_input_strings
else:
    from transformation.db_input import db_input_fields
    from extraction.text_extractor import retrieve_input_strings

def extract(report_batch_filenames : list) -> pd.DataFrame:
    # pdfs loaded from report test batch file
    pdfs = [pymupdf.open(filename) \
        for filename in report_batch_filenames]
    # init report df
    report_df = pd.DataFrame(columns=db_input_fields)
    
    # extract data into report_df foreach pdf into foreach row
    for i, pdf in enumerate(pdfs):
        input_data = retrieve_input_strings(pdf)
        
        file_name = os.path.basename(report_batch_filenames[i])
        # relative_path = os.path.join('reports', file_name)
        # relative_path = f"./reports/{file_name}"
        input_data['Report_path'] = file_name
        pdf.save(os.path.join(os.getcwd(), 'app', 'static', 'reports', file_name))
        
        
        # print(report_df.columns, '\n', input_data.keys())
        report_df.loc[len(report_df)] = input_data
        # print(report_df['Report_path'])
        
        
    # print("fin")
    print(report_df)
    return report_df

if __name__ == "__main__":
    extract(report_folder=r'.\others\test_reports_batch')
    pass