
import os
import json
import logging

from filetools.formats import sqlite
from filetools.formats import jsonline

from filetools.utils import get_meta
from filetools.utils import scan_files

logger = logging.getLogger(__name__)


class Scanner:

    def __init__(self, path:str, output_type:str, output_file:str, ignore_tags:list) -> None:

        if not os.path.exists(path) or not os.path.isdir(path):
            raise ValueError('The directory does not exist or not a directory, {}'.format(path))

        self._path = path
        if not output_type or output_type not in ('jsonline', 'sqlite3'):
            raise ValueError(f'The output type must be jsonline or sqlite3, founded: {output_type}')

        if output_type == 'jsonline':
            self._metastore = jsonline.Metastore(output_file)
        else:
            self._metastore = sqlite.Metastore(output_file)
        self._ignore_tags = ignore_tags

    def scan_files(self):
        ''' run scanner for getting files metadata
        '''
        try:
            total_files = 0
            for filepath in scan_files(self._path):
                total_files += 1
                meta = get_meta(filepath, ignore_tags=self._ignore_tags)
                meta['tags'] = json.dumps(meta['tags'])
                self._metastore.put(meta)
                if total_files % 1000 == 0:
                    logger.info("Processed {} files".format(total_files))
                    self._metastore.commit()
            self._metastore.commit()
            logger.info('Total processed files: {}'.format(total_files))
        except KeyboardInterrupt:
            print("Interrupted by user")

    def stats(self):
        ''' returns statistics for path
        '''
        try:
            total_files = 0
            total_directories = 0
            for filepath in scan_path(self._path):
                total_files += 1
                meta = get_meta(filepath, ignore_tags=self._ignore_tags)
                meta['tags'] = json.dumps(meta['tags'])
                self._metastore.put(meta)
                if total_files % 1000 == 0:
                    logger.info("Processed {} files".format(total_files))
                    self._metastore.commit()
            self._metastore.commit()
            logger.info('Total processed files: {}'.format(total_files))
        except KeyboardInterrupt:
            print("Interrupted by user")


    def close(self):
        ''' complete work with scanner
        '''
        self._metastore.close()
        self._metastore = None
