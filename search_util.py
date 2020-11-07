import os
import sqlite3

DATABASE_PATH = os.path.join('data', 'lexicalbundle.db')

SELECT_NEXT_WORD = '''
SELECT next_word, next_word_pos, count FROM LB_{N}gram 
WHERE query = "{query}"
ORDER BY count DESC
LIMIT {limit};
'''

def search_nextword(query: str, limit):
    response = {}

    limit = limit if limit else 10
    results = search_db(query, limit)

    # result format: [[({2gram word}, {2gram pos}, {2gram count})], [...{3gram}], [...{4gram}], [...{5gram}], [...{6gram}]]
    for idx, ngram_result in enumerate(results, 2):
        response[idx] = []
        for next_word, next_word_pos, count in ngram_result:
            response[idx].append({
                "next_word": next_word,
                "next_word_pos": next_word_pos,
                "count": count
            })
    return response

def search_db(tokens, limit):
    results = []
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        for n in range(2,7):
            if (n-1) > len(tokens):
                results.append([])
                continue

            sql_query = SELECT_NEXT_WORD.format(N=n,
                                                query=' '.join(tokens[0-(n-1):]),
                                                limit=limit)
            cursor = conn.execute(sql_query)
            conn.commit()
            results.append(cursor.fetchall())
    finally:
        conn.close()
    return results