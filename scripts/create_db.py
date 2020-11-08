import os

from utils.LogHelper import LogHelper
from utils.SQLUtilities import SQLHandler

# --- SETTING --- #
DATABASE_PATH = os.path.join('data', 'lexicalbundle.db')
DATA_PATH = os.path.join('corpus', 'lexicalbundle', 'lexicalbundle.{N}.txt')
LOG_PATH = os.path.join('log', 'creat_lexicalbundle_db.{N}.log')

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
CREATE INDEX idx_LB_{N}gram ON LB_{N}gram (query);
'''

# --- MAIN --- #
if __name__ == '__main__':
    from argparse import ArgumentParser
    def parse_args():
        parser = ArgumentParser()
        parser.add_argument('n', type=int, nargs='+', choices=[2, 3, 4, 5, 6], help='ngram')
        parser.add_argument('-b', '--batch-size', type=int, default=5000, help='Tx batch size')
        parser.add_argument('-v', '--verbose', type=int, default=2, help='verbose level')
        return parser.parse_args()
    args = parse_args()

    sql_handler = SQLHandler(DATABASE_PATH, debugging=(args.verbose==3))

    for n in args.n:
        logger = LogHelper(log_level=args.verbose, log_file=LOG_PATH.format(N=n))
        logger.log('info', f'processing {n} gram file...')
        f = open(DATA_PATH.format(N=n), 'r', encoding='utf-8')

        # create tables
        query = CREATE_NGRAM_TABLE.format(N=n)
        logger.log('debug', f'SQL QUERY: {query}')
        sql_handler.execute(query)

        sql_count = 0
        sql_queries = []
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
            sql_queries.append(sql_query)
            sql_count += 1

            if sql_count == args.batch_size:
                sql_handler.execute(sql_queries)
                sql_queries = []
                sql_count = 0
        
        if sql_count:
            sql_handler.execute(sql_queries)

        # create index to speed up searching
        sql_query = CREATE_QUERY_INDEX.format(N=n)
        sql_handler.execute(sql_query)

        f.close()
