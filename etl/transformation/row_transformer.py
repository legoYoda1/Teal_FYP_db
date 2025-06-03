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
        temp = report_batch_row["Location"]
        report_batch_row["Landmark"] = ''.join(temp[-4:])
        report_batch_row["Location"] = ''.join(temp[:-7])
        
    except Exception as e:
        print(f"Error: {e}")
        raise
        
            
    # convert date to date_key format
    try:
        report_batch_row["Date"] = format_to_date_key(report_batch_row["Date"])
        report_batch_row["Reported_via__date"] = format_to_date_key(report_batch_row["Reported_via__date"])
        report_batch_row["Acknowledgement__date"] = format_to_date_key(report_batch_row["Acknowledgement__date"])
    except Exception as e:
        print(f"Error: {e}")
        raise
        
        
    # omit strings(words) from quantity/measurement and convert to int
    try:
        # report_batch_row["Quantity"] = int(*report_batch_row["Quantity"].split()[0])
        # report_batch_row["Measurement"] = int(*report_batch_row["Measurement"].split()[0])
        pass
        
    # except Exception as e:
    #     # print(f"Error: {e}")
    #     raise
    # try:
    #     is_repeated_defect = report_batch_row["Repeated_defect"]
    #     if is_repeated_defect == "Yes": 
    #         report_batch_row["Repeated_defect"] = 1
    #     else:
    #         report_batch_row["Repeated_defect"] = 0
            
    except Exception as e:
        # print(f"Error: {e}")
        raise

        
    
    return report_batch_row
    
if __name__ == "__main__":
    pass
    