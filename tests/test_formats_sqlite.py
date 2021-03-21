
import json
import pytest

from filetools.formats.sqlite import Metastore, SQLiteDatabase

RECORD = {
    'sha256': '5b78afc1c065a1eecbbdb847a30cb1bea163a6ec4a2a8225fd3ca1eb2f952536',
    'path': 'tests/resourses/data.file',
    'name': 'data.file',
    'ext': '.file',
    'size': 17079235,
    'tags': json.dumps(['tests', 'resources'])
}


# ===================================================
# SQLiteDatabase
#

def test_db_init(tmpdir):
    ''' test for sqlite db init
    '''
    path = tmpdir / 'db.sqlite3'
    db = SQLiteDatabase(path)
    assert db
    assert db.connection
    assert db.cursor

def test_db_init_no_path():
    ''' test for sqlite db init with no path
    '''
    with pytest.raises(RuntimeError):
        SQLiteDatabase(None)

def test_db_execute_and_query_methods(tmpdir):
    ''' test for execute and query methods
    '''
    path = tmpdir / 'db.sqlite3'
    db = SQLiteDatabase(path)
    db.execute('CREATE TABLE test (key INTEGER, value BLOB)')
    db.execute('INSERT INTO test (key, value) VALUES (:key, :value)', {'key': 1, 'value': 'Value#1'})
    db.commit()
    assert list(db.query('SELECT * FROM test')) == [
        {'key': 1, 'value': 'Value#1'}
    ]
    db.close()

# ===================================================
# Metastore
#

def test_metastore_init(tmpdir):
    ''' test for metastore init
    '''
    path = tmpdir / 'metastore.sqlte3'
    metastore = Metastore(path)
    assert metastore

def test_metastore_put_and_get_methods(tmpdir):
    ''' test for metastore put and get methods
    '''
    path = tmpdir / 'metastore.sqlite3'
    metastore = Metastore(path)
    metastore.put(RECORD)
    metastore.commit()
    assert list(metastore.get()) == [RECORD, ]
    metastore.close()
