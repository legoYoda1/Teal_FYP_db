import pandas as pd
import random
import string
from datetime import datetime, timedelta

# Helper functions
def generate_id(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def random_date(start, end):
    """Generate a random date between start and end in YYYYMMDD format"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime('%Y%m%d')

def random_name():
    first_names = ['John', 'Jane', 'Alex', 'Emily', 'Chris', 'Nina', 'David', 'Sarah', 'James', 'Lily']
    last_names = ['Smith', 'Tan', 'Lee', 'Ng', 'Lim', 'Wang', 'Zhang', 'Chan', 'Brown', 'Johnson']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_defect_rows(n=10):
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 5, 19)
    
    rows = []
    for _ in range(n):
        date_reported = random_date(start_date, end_date)
        row = {
            'Defect_ref_no': generate_id(),
            'Date': date_reported,
            'Repeated_defect': random.choice(['1', '0']),
            'Type_of_road': '',
            'Location': '',
            'Landmark': '',
            'Type_of_asset': '',
            'Description': random.choice(['Crack on edge', 'Minor pothole', 'Worn paint']),
            'Quantity': random.randint(1, 5),
            'Measurement': random.randint(1, 5),
            'Cause_of_defect': random.choice(['Weathering', 'Heavy load', 'Aging']),
            'Recommendation': random.choice(['Seal crack', 'Patch area', 'Repaint lines']),
            'Inspected_by': random_name(),
            'Supervised_by': random_name(),
            'Reported_via__method': random.choice(['Phone', 'Email', 'Online']),
            'Reported_via__agency': random.choice(['Public', 'Contractor']),
            'Reported_via__date': date_reported,
            'Reported_via__time': f"{random.randint(0,23):02}{random.randint(0,59):02}",
            'Acknowledgement__method': random.choice(['Phone', 'Email', 'Online']),
            'Acknowledgement__date': date_reported,
            'Acknowledgement__time': f"{random.randint(0,23):02}{random.randint(0,59):02}",
            'Defects_verified_by__name': random_name(),
            'Defects_verified_by__date': date_reported,
            'Instructions': random.choice(['Monitor closely', 'Fix within 2 days', 'Urgent attention']),
            'WSO_no': generate_id(),
            'Acknowledged_and_received_by__name': random_name(),
            'Acknowledged_and_received_by__date': date_reported
        }
        rows.append(row)
    
    return pd.DataFrame(rows)


if __name__ == "__main__":
    try:
        df = generate_defect_rows(n=20)
        df.to_csv(r'others/misc/dummy_report_batch.csv', index=False)  
    except Exception as e:
        raise