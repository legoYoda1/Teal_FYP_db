import pandas as pd
import random
import string
from datetime import datetime, timedelta

# Helper functions
def generate_id(length=10):
    compass_directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    id = compass_directions[random.randint(0, 7)] + '-'  \
        + 'MAS' + str(random.randint(1, 3)) + '-' \
        + 'EXT-WK'+ str(random.randint(1, 100)).zfill(3) + '-' \
        + str(random.randint(1, 50)).zfill(3)
    
    return id

def random_date(start, end):
    """Generate a random date between start and end in YYYYMMDD format"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%d/%m/%Y")

def random_name():
    first_names = ['John', 'Jane', 'Alex', 'Emily', 'Chris', 'Nina', 'David', 'Sarah', 'James', 'Lily']
    last_names = ['Smith', 'Tan', 'Lee', 'Ng', 'Lim', 'Wang', 'Zhang', 'Chan', 'Brown', 'Johnson']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_defect_rows(n=10):
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 5, 19)
    
    singapore_roads = [
    "Orchard Road",
    "Bukit Timah Road",
    "Holland Road",
    "Serangoon Road",
    "Tampines Avenue 5",
    "Cecil Street",
    "Jurong West Street 91",
    "Sembawang Road",
    "Upper Thomson Road",
    "Changi Road"
    ]
    
    rows = []
    for _ in range(n):
        date_reported = random_date(start_date, end_date)
        row = {
            'Defect_ref_no': generate_id(),
            'Date': date_reported,
            'Repeated_defect': random.choice(['1', '0']),
            'Type_of_road': random.choice(["Street", "Avenue", "Expressway", "Drive"]),
            'Location': random.choice(singapore_roads),
            'Landmark': 'LP'+str(random.randint(1, 20)).zfill(3) + random.choice(['A', 'B', 'C', 'D', 'E', 'F']) ,
            'Type_of_asset': random.choice(["kerb", "paint_spillage", "trench", "drainage", "missing_sign", "pothole"]),
            'Description': random.choice(['Mild defect', 'Medium defect', 'Severe defect']),
            'Quantity': random.randint(1, 5),
            'Measurement': f"{random.randint(1, 5)}m x {random.randint(1, 5)}m",
            'Cause_of_defect': random.choice(['Weathering', 'Heavy load', 'Aging']),
            'Recommendation': random.choice(['Seal crack', 'Patch area', 'Repaint lines']),
            'Inspected_by': random_name(),
            'Supervised_by': random_name(),
        }
        rows.append(row)
    
    return pd.DataFrame(rows)


if __name__ == "__main__":
    try:
        df = generate_defect_rows(n=1)
        df.to_csv(r'others/misc/dummy_report_batch.csv', index=False)  
    except Exception as e:
        raise