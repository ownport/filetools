
import pytest

from filetools.formats.jsonline import Metastore

RECORD = {
    'sha256': '5b78afc1c065a1eecbbdb847a30cb1bea163a6ec4a2a8225fd3ca1eb2f952536',
    'path': 'tests/resourses/data.file',
    'name': 'data.file',
    'ext': '.file',
    'size': 17079235,
    'tags': ['tests', 'resources']
}

def test_metastore_init_no_path():
    ''' test jsonline metastore_init with no path
    '''
    with pytest.raises(RuntimeError):
        Metastore(None)

def test_metastore_init(tmpdir):
    ''' test jsonline metastore init
    '''
    path = tmpdir / 'metastore.jsonline'
    metastore = Metastore(path)
    assert metastore
    metastore.close()

def test_metastore_put_method(tmpdir):
    ''' test jsoneline metastore put method
    '''
    path = tmpdir / 'metadata.jsonline'
    metastore = Metastore(path)
    metastore.put(RECORD)
    metastore.commit()
    # assert list(metastore.get()) == [RECORD,]
    metastore.close()    
