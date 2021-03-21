
import os
import sys
import json
import logging
import argparse

from filetools.formats import sqlite
from filetools.formats import jsonline

from filetools.utils import get_meta
from filetools.utils import scan_directory

logger = logging.getLogger(__name__)


class Scanner:

    def __init__(self, args) -> None:
        parser = argparse.ArgumentParser(description='scan files into the directory for metadata')
        parser.add_argument('--path', dest='path', required=True,
                            help="the path to the directory for file scanning")
        parser.add_argument('--output-type', dest='output_type',
                            choices=['jsonline', 'sqlite3'],
                            help="the output type, possible options: jsonline or sqlite3")
        parser.add_argument('--output-file', dest='output_file',
                            help="the path output file for storing metadata")
        parser.add_argument('--ignore-tag', dest='ignore_tags', action='append',
                            help='the tags for ignoring')
        _args = parser.parse_args(args)

        if not os.path.exists(_args.path) or not os.path.isdir(_args.path):
            parser.print_usage()
            logger.error('The directory does not exist or not directory, {}'.format(_args.path))
            sys.exit(1)

        self._path = _args.path
        if _args.output_type == 'jsonline':
            self._metastore = jsonline.Metastore(_args.output_file)
        else:
            self._metastore = sqlite.Metastore(_args.output_file)
        self._ignore_tags = _args.ignore_tags

    def run(self):
        ''' run scanner
        '''
        try:
            total_files = 0
            for filepath in scan_directory(self._path):
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
