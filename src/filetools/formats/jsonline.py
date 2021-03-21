
import os
import json

class Metastore:

    def __init__(self, path:str) -> None:
        
        if not path:
            raise RuntimeError('No path to Jsonline database')
        self._db = open(path, 'w')

    def put(self, metadata:dict) -> None:
        ''' store file metadata in the metastore
        '''
        self._db.write('{}\n'.format(json.dumps(metadata)))

    # def get(self):
    #     ''' get all file metadata from the metastore
    #     '''
    #     self._db.seek(0)
    #     for metadata in self._db.readlines():
    #         yield json.loads(metadata)

    def commit(self):
        pass

    def close(self):
        ''' close metastore connection
        '''
        self._db.close()
