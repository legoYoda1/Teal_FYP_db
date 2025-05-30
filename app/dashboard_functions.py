import requests
import numpy as np

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


def get_chart_suggestions(df, query, url='http://localhost:1234/v1/chat/completions'):
    payload = {
    "model": "deepseek-coder-6.7b-instruct",
    "messages": [
        {
            "role": "system",
            "content": "You are a Python data visualization assistant. Given a pandas DataFrame and the sql query used to obtain it, suggest a useful plotly chart that the user will be able to generate using the data in the dataframe to aid in analytics. Respond in valid JSON only, with two keys: title (string) and code (string). The code must only include the full plotly code to generate the plot, and The code must assign the Plotly figure to a variable named fig. Do not add fig.show() at the end of the code."
        },
        {
            "role": "user",
            "content": "DataFrame preview:\n" + df.head().to_string() + "\n\nSQL Query:\n" + query
        }
    ],
    "temperature": 0.3,
    "max_tokens": 1024,
    "stream": False
}

    response = requests.post(url=url, json=payload)
    response_json = response.json()
    return response_json['choices'][0]['message']['content']


def convert_ndarrays(obj):
    if isinstance(obj, dict):
        return {k: convert_ndarrays(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_ndarrays(v) for v in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj