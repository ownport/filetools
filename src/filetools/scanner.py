
import os
import json
import logging
import pathlib

from collections import Counter

from filetools.formats import sqlite
from filetools.formats import jsonline

from filetools.utils import get_meta
from filetools.utils import scan_files
from filetools.utils import progress_bar
from filetools.libs.tabulate import tabulate

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
        processed_files = 0
        total_files = self.stats().get('total files')
        
        try:
            progress_bar(processed_files, total_files)
            for filepath in scan_files(self._path):
                processed_files += 1
                meta = get_meta(filepath, ignore_tags=self._ignore_tags)
                meta['tags'] = json.dumps(meta['tags'])
                self._metastore.put(meta)
                if processed_files % 100 == 0:
                    progress_bar(processed_files, total_files)
                    self._metastore.commit()
            self._metastore.commit()
            print()
            print(tabulate((
                    ('Processed files', processed_files),
                    ('Total files', total_files)
                ),tablefmt='github')
            )
        except KeyboardInterrupt:
            print("Interrupted by user")

    def stats(self):
        ''' scan directory for gettings statistics
        returns the next metrics:
        - total files
        - total directories
        - total size
        '''
        try:
            metrics = Counter()
            for root, _, files in os.walk(self._path):
                metrics['total files'] += len(files)
                metrics['total directories'] += 1
                for filename in files:
                    metrics['total size'] += pathlib.Path(os.path.join(root, filename)).stat().st_size
            return dict(metrics)
        except KeyboardInterrupt:
            print("Interrupted by user")

    def close(self):
        ''' complete work with scanner
        '''
        self._metastore.close()
        self._metastore = None
