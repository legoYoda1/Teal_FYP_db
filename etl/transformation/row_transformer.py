from datetime import datetime
import pandas as pd

# # sets respective year/month/days keypair from date keypair
def format_to_date_key(date : str) -> None:
    # print(pd.isna(date))
    # print(pd.isnull(date))
    
    if pd.isna(date) or pd.isnull(date):
        return None
    
    try:
        # print(date)
        date_object = datetime.strptime(date, "%d/%m/%Y")
        date_elements = date_object.strftime("%d/%m/%Y").split('/')
        date = date_elements[2] + date_elements[1] + date_elements[0] 
        
    except Exception as e:
        print(f"Error: {e}")
        # raise
    
    return date
    
def preprocess_report_batch_row(report_batch_row: pd.Series) -> pd.Series:
    
    # split location and landmark from "Location" key, put landmark in "Landmark"
    try:
        temp = report_batch_row["location"].split()
        report_batch_row["landmark"] = ' '.join(temp[-2:])
        report_batch_row["location"] = ' '.join(temp[:-2])
        
    except Exception as e:
        print(f"Error: {e}")
        raise
        
            
    # convert date to date_key format
    try:
        report_batch_row["date"] = format_to_date_key(report_batch_row["date"])
    except Exception as e:
        print(f"Error: {e}")
        raise
        
        
    # omit strings(words) from quantity/measurement and convert to int
    try:
        report_batch_row["quantity"] = int(*report_batch_row["quantity"].split()[0])
        report_batch_row["measurement"] = int(*report_batch_row["measurement"].split()[0])
        
    except Exception as e:
        # print(f"Error: {e}")
        raise
    try:
        is_repeated_defect = report_batch_row["repeated_defect"]
        if is_repeated_defect == "Yes": 
            report_batch_row["repeated_defect"] = 1
        else:
            report_batch_row["repeated_defect"] = 0
            
    except Exception as e:
        # print(f"Error: {e}")
        raise

    try:
        is_repeated_defect = report_batch_row["repeated_defect"]
        if is_repeated_defect == "Yes": 
            report_batch_row["repeated_defect"] = 1
        else:
            report_batch_row["repeated_defect"] = 0
            
    except Exception as e:
        # print(f"Error: {e}")
        raise
        
    
    return report_batch_row
    
if __name__ == "__main__":
    pass
    