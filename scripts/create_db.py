import os
import sqlite3

# --- SETTING --- #
DATABASE_PATH = os.path.join('data', 'collocation.db')
DATA_PATH = os.path.join('data', 'collocation', 'collocation.filtered.txt')

# --- SQL TEMPLATE --- #
CREATE_TABLE = '''
CREATE TABLE collocations (
    cid INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT,
    collocation TEXT,
    dist_info TEXT
);
'''
INSERT_COLLOCATION = '''
INSERT INTO collocations (word, collocation, dist_info)
VALUES ("{word}", "{collocation}", "{dist}")
'''

# --- MAIN --- #
f = open(DATA_PATH, 'r', encoding='utf-8')
conn = sqlite3.connect(DATABASE_PATH)

conn.execute(CREATE_TABLE)
conn.commit()

for line in f:
    line = line.strip()
    _, collocation, dist_str = line.split('\t')
    collocation, _ = collocation.split('|')
    center_word, col_word = collocation.split(' ')

    sql_query = INSERT_COLLOCATION.format(word=center_word,
                                          collocation=col_word,
                                          dist=dist_str)
    conn.execute(sql_query)
    conn.commit()

f.close()
conn.close()