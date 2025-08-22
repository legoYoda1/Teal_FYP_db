import requests
import numpy as np
import json
import hashlib
from flask import current_app
import os
from dotenv import load_dotenv
load_dotenv()

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


def refresh_dropbox_token():
    """Secure Dropbox token refresh with proper error handling"""
    url = "https://api.dropbox.com/oauth2/token"
    
    # Ensure no whitespace in credentials
    data = {
        "grant_type": "refresh_token",
        "refresh_token": os.getenv('DROPBOX_REFRESH_TOKEN').strip(),
        "client_id": os.getenv('DROPBOX_APP_KEY').strip(),
        "client_secret": os.getenv('DROPBOX_APP_SECRET').strip()
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    try:
        response = requests.post(url, data=data, headers=headers, timeout=30)
        response.raise_for_status()  # Raises HTTPError for 4XX/5XX
        return response.json()["access_token"]
    
    except requests.exceptions.HTTPError as e:
        error_detail = e.response.json() if e.response.text else {}
        current_app.logger.error(
            f"Dropbox token refresh failed - {e.response.status_code}\n"
            f"Error: {error_detail.get('error', 'Unknown')}\n"
            f"Description: {error_detail.get('error_description', 'No details')}"
        )
        raise

def get_dropbox_token():
    if 'token' in current_app.dropbox_token_cache:
        return current_app.dropbox_token_cache['token']
    
    # Refresh logic here...
    new_token = refresh_dropbox_token()
    current_app.dropbox_token_cache['token'] = new_token
    return new_token




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