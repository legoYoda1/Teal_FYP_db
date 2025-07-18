import requests
import numpy as np
import json
import hashlib

# Naive in-memory cache (clears on server restart)
query_cache = {}

def get_cache_key_from_query(query: str, params: dict = None) -> str:
    """
    Generate a hash key based on the query and optional parameters.
    """
    key_str = query.strip()
    if params:
        try:
            key_str += json.dumps(params, sort_keys=True)
        except Exception:
            pass  # If params can't be serialized, skip it
    return hashlib.md5(key_str.encode()).hexdigest()

def insert_filters(query, filters_clause):
    """
    Insert filters before GROUP BY / ORDER BY / LIMIT if they exist.
    """
    # Keywords we care about
    keywords = ['GROUP BY', 'ORDER BY', 'LIMIT']
    upper_query = query.upper()
    
    # Find the earliest keyword position
    min_pos = len(query)
    insert_pos = len(query)
    for kw in keywords:
        pos = upper_query.find(kw)
        if pos != -1 and pos < min_pos:
            min_pos = pos
            insert_pos = pos

    # If there's already a WHERE clause, insert with AND
    if 'WHERE' in upper_query:
        return query[:insert_pos] + ' AND ' + filters_clause + ' ' + query[insert_pos:]
    else:
        return query[:insert_pos] + ' WHERE ' + filters_clause + ' ' + query[insert_pos:]
    
    # export the function


def convert_ndarrays(obj):
    if isinstance(obj, dict):
        return {k: convert_ndarrays(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_ndarrays(v) for v in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj
    
def get_query_suggestions(prompt, url='http://localhost:1234/v1/chat/completions'):
    payload = {
    "model": "deepseek-coder-6.7b-instruct",
    "messages": [
        {
            "role": "system",
            "content": "You are a data engineer. Given a natural language prompt, generate a SQL query that retrieves the data needed to answer the question from the data warehouse. The query should be valid SQLite syntax, without any comments. Make sure to follow the table and column names as per the data warehouse schema. Data warehouse schema: Tables: date_dim(date_id PK, day, month, year), time_dim(time_id PK, minute, hour), location_dim(location_id PK, zone, location, lamppost_id, road_type), asset_dim(asset_id PK, asset_type), supervisor_dim(supervisor_id PK, name), inspector_dim(inspector_id PK, name), report_fact(report_id PK, defect_ref_no, date_id → date_dim.date_id, time_id → time_dim.time_id, location_id → location_dim.location_id, asset_id → asset_dim.asset_id, supervisor_id → supervisor_dim.supervisor_id, inspector_id → inspector_dim.inspector_id, repeated_defect, description, quantity, measurement, cause_of_defect, recommendation, report_path)."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    "temperature": 0.3,
    "max_tokens": 1024,
    "stream": False
}

    response = requests.post(url=url, json=payload)
    response_json = response.json()
    content = response_json['choices'][0]['message']['content']

    # Try to parse content as JSON. If it has a top-level "query" key, return that.
    try:
        parsed = json.loads(content)
        # If parsed is a dict with a "query" field, extract it:
        if isinstance(parsed, dict) and "query" in parsed:
            return parsed["query"]
    except json.JSONDecodeError:
        pass

    # Fallback: return the raw text if it wasn’t valid JSON
    return content