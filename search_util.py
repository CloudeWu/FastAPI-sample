import os
import sqlite3

DATABASE_PATH = os.path.join('data', 'collocation.db')

SELECT_WORD = '''
SELECT collocation, dist_info FROM collocations
WHERE word = "{word}";
'''

def search_collocation(word: str, limit):
    response = {}

    results = search_db(word)
    limit = limit if limit else len(results)
    # result format: [({collocation}, {dist_info})]
    for idx, (collocation, dist_str) in enumerate(results):
        if idx >= limit:
            break
        response[collocation] = dist_str
    return response

def search_db(word):
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        sql_query = SELECT_WORD.format(word=word)
        cursor = conn.execute(sql_query)
        conn.commit()
        results = cursor.fetchall()
    finally:
        conn.close()
    return results