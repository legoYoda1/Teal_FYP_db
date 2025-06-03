import pandas as pd
import random
import string
import os
from datetime import datetime, timedelta

import pymupdf

def clear_folder():
    for filename in os.listdir(r'.\others\test_reports_batch'):
        file_path = os.path.join(r'.\others\test_reports_batch', filename)
        if os.path.isfile(file_path):  # Make sure it's a file, not a folder
            os.remove(file_path)
            
input_cood = {
 'Defect_ref_no': (148, 98),
 'Date': (416, 96),
 'Repeated_defect': (225, 121),
 'Type_of_road': (225, 147),
 'Location': (173, 173),
 'Landmark': (300, 173),
 'Type_of_asset': (173, 201),
 'Description': (173, 228),
 'Quantity': (173, 255),
 'Measurement': (173, 281),
 'Cause_of_defect': (173, 306),
 'Recommendation': (173, 333),
 'Inspected_by': (173, 357),
 'Supervised_by': (173, 396)
}

  
# form_input_boundary = {
#     "Defect_ref_no": (148, 83, 310, 103),
#     "Date": (416, 81, 564, 101),
#     "Repeated_defect": (225, 109, 311, 126),
#     "Type_of_road": (225, 134, 354, 152),
#     "Location": (173, 160, 521, 178),
#     "Type_of_asset": (173, 186, 521, 206),
#     "Description": (173, 215, 521, 233),
#     "Quantity": (173, 239, 521, 260),
#     "Measurement": (173, 264, 521, 286),
#     "Cause_of_defect": (173, 291, 521, 311),
#     "Recommendation": (173, 317, 521, 338),
#     "Inspected_by": (173, 342, 310, 362),
#     "Supervised_by": (173, 380, 310, 401),
# }            
            

import sys
if __name__ == "__main__":
    # from extraction.text_extractor import retrieve_input_strings
    
    try:
        df = pd.read_csv(r'.\others\misc\dummy_report_batch.csv')
        clear_folder() 
        
        for i in range(len(df)):
            pdf = pymupdf.open(r'.\others\template_og.pdf')
            page = pdf[0]  
            for col in df.columns:
                value = df.at[i, col]
                page.insert_text(input_cood[col], str(value), fontsize=12, fontname="helv")
                # print(f"Column: {col}, Value: {value}")
            
            
            # print(retrieve_input_strings(pdf))
            filepath = os.path.join(r'.\others\test_reports_batch', f'{i}.pdf')
            pdf.save(filepath)
    
    except Exception as e:
        raise