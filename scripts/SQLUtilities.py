import sqlite3

class SQLHandler(object):
    def __init__(self, database, debugging=False):
        self.database = database
        self._debugging = debugging

    def execute(self, queries):
        queries = queries if isinstance(queries, list) else [queries]
        results = []

        conn = sqlite3.connect(self.database)
        try:
            for query in queries:
                self.log('debug', f'Exec query: {query}')
                cursor = conn.execute(query)
                results.append(cursor.fetchall())
            self.log('debug', 'Tx commit')
            conn.commit()
        except Exception as e:
            self.log('warn', f'commit rollback: {queries}')
            self.log('warn', e)
        conn.close()

        return results
    
    def log(self, tag, message):
        if tag.upper() == 'DEBUG' and not self._debugging:
            return
        print(f' [ {tag.upper()} ] {message}')