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
