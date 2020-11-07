import os

from LogHelper import LogHelper
from SQLUtilities import SQLHandler

# --- SETTING --- #
DATABASE_PATH = os.path.join('data', 'lexicalbundle.db')
DATA_PATH = os.path.join('data', 'lexicalbundle', 'lexicalbundle.{N}.txt')
LOG_PATH = os.path.join('log', 'creat_db.log')

# --- SQL TEMPLATE --- #
CREATE_NGRAM_TABLE = '''
CREATE TABLE LB_{N}gram (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    pos TEXT,
    next_word TEXT,
    next_word_pos TEXT,
    count INT
);
'''
INSERT_LEXICALBUNDLE = '''
INSERT INTO LB_{N}gram (query, pos, next_word, next_word_pos, count) 
VALUES ("{query}", "{pos}", "{next_word}", "{next_word_pos}", {count});
'''
CREATE_QUERY_INDEX = '''
CREATE INDEX idx_LB_{N}gram ON {N}gram (query);
'''

# --- MAIN --- #
sql_handler = SQLHandler(DATABASE_PATH)
logger = LogHelper(log_level=1, log_file=LOG_PATH)

for n in range(2,7):
    logger.log('info', f'processing {n} gram file...')
    f = open(DATA_PATH.format(N=n), 'r', encoding='utf-8')

    # create tables
    query = CREATE_NGRAM_TABLE.format(N=2)
    logger.log('debug', f'SQL QUERY: {query}')
    sql_handler.execute(query)

    for line in f:
        line = line.strip()
        count, lexicalbundle, pos = line.split('\t')

        # extract query and recommand word
        try:
            query, next_word = lexicalbundle.rsplit(' ', 1)
            pos, next_word_pos = pos.rsplit(' ', 1)
            count = int(count)
        except ValueError:
            logger.log('warn', f'VALUE ERROR: {line}')
            continue
        except IndexError:
            logger.log('warn', f'INDEX ERROR: {line}')
            continue
        logger.log('debug', f'query: {query} ({pos}); next_word: {next_word} ({next_word_pos})')
        
        # insert database
        sql_query = INSERT_LEXICALBUNDLE.format(N=n,
                                                query=query,
                                                pos=pos,
                                                next_word=next_word,
                                                next_word_pos=next_word_pos,
                                                count=count)
        logger.log('debug', f'SQL QUERY: {sql_query}')
        sql_handler.execute(sql_query)
    
    # create index to speed up searching
    logger.log('debug', 'creating index tables...')
    sql_query = CREATE_QUERY_INDEX.format(N=n)
    sql_handler.execute(sql_query)

    f.close()
