
import sqlite3

# SQL Statements
SQL_CREATE_FILES_TABLE = '''
CREATE TABLE IF NOT EXISTS files (
    sha256      STRING,
    path        STRING,
    name        STRING,
    ext         STRING,
    size        INTEGER,
    tags        BLOB
)
'''
SQL_INSERT_METADATA = '''
INSERT INTO files (
    sha256, path, name, ext, size, tags
) VALUES (
    :sha256, :path, :name, :ext, :size, :tags
)
'''

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLiteDatabase:

    def __init__(self, path:str) -> None:
        ''' init sqlite database
        '''
        if not path:
            raise RuntimeError('No path to SQLite database')
        
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = dict_factory
        self._cursor = self._conn.cursor()

    @property
    def connection(self) -> sqlite3.Connection:
        ''' returns connection reference
        '''
        return self._conn

    @property
    def cursor(self) -> sqlite3.Cursor:
        ''' returns cursor reference
        '''
        return self._cursor

    def execute(self, stmt:str, params:dict=None) -> None:
        ''' execute the statement
        '''
        if params:
            self.cursor.execute(stmt, params)
        else:
            self.cursor.execute(stmt)

    def query(self, stmt:str, params=None):
        ''' execute the statement and return result
        '''
        self.execute(stmt, params)
        for record in self.cursor.fetchall():
            yield record

    def commit(self):
        ''' commit changes
        '''
        self._conn.commit()

    def close(self):
        ''' close connection
        '''
        self._conn.close()


class Metastore:

    def __init__(self, path:str) -> None:
        
        self._db = SQLiteDatabase(path)
        self._db.execute(SQL_CREATE_FILES_TABLE)

    def put(self, metadata):
        ''' store file metadata in the metastore
        '''
        self._db.execute(SQL_INSERT_METADATA, metadata)

    def get(self):
        ''' rreturn list of files
        '''
        for metadata in self._db.query('SELECT * FROM files'):
            yield metadata
    
    def commit(self):
        ''' commit changes
        '''
        self._db.commit()

    def close(self):
        ''' close metastore connection
        '''
        self._db.close()

