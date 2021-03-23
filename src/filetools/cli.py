
import os
import sys
import logging
import argparse

from collections import Counter
from typing import DefaultDict

from filetools import utils
from filetools.scanner import Scanner
from filetools.version import version
from filetools.utils import convert_size
from filetools.libs.tabulate import tabulate


FILETOOLS_USAGE = '''filetools <command> [<args>]
The list of commands:
    stats       collect statistics about files in the directory
    scan        scan files into the directory for metadata           
    info        collect metedata from the file        
    normalize   normalize filenames
'''

logger = logging.getLogger(__name__)


class CLI():

    def __init__(self):
        parser = argparse.ArgumentParser(usage=FILETOOLS_USAGE)
        parser.add_argument('-v', '--version', action='version',
                            version='filetools-v{}'.format(version))
        parser.add_argument('-l', '--log_level', default='DEBUG',
                            help='Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print('Unrecognized command: %s' % args.command)
            sys.exit(1)

        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s (%(name)s) [%(levelname)s] %(message)s")

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()


    @staticmethod
    def scan():
        ''' scan directory for collecting files metadata
        '''
        scanner = Scanner(sys.argv[2:])
        scanner.run()

    @staticmethod
    def stats():
        ''' scan directory for collection general stats about files
        '''
        parser = argparse.ArgumentParser(description='scan files into the directory for metadata')
        parser.add_argument('--path', dest='path', required=True,
                            help="the path to the directory for file scanning")
        parser.add_argument('--sort-by', dest='sort_by', default='size',
                            choices=['files', 'size'],
                            help="sort output by number or files or size")
        args = parser.parse_args(sys.argv[2:])

        if not os.path.exists(args.path) or not os.path.isdir(args.path):
            parser.print_usage()
            logger.error('The directory does not exist or not directory, {}'.format(args.path))
            sys.exit(1)

        try:
            files = 0
            stats = DefaultDict(lambda: DefaultDict(int))
            for filepath in utils.scan_directory(args.path):
                files  += 1
                ext = os.path.splitext(filepath)[1]
                stats[ext]['files'] += 1
                stats[ext]['size'] += os.stat(filepath).st_size

            data = [(ext, info['files'], info['size'] ) for ext, info in stats.items()]
            sorting_field_id = 1 if args.sort_by == 'files' else 2 # if by size
            data = sorted(data, key=lambda x: x[sorting_field_id], reverse=True)
            data = [(ext, files, convert_size(size)) for ext, files, size in data]
            print()
            print(tabulate(
                    data, 
                    headers=['Extension', "Files", "Size"], 
                    tablefmt="github")
            )
            print(f"\nTotal files: {files}")

        except KeyboardInterrupt:
            print("Interrupted by user")

    @staticmethod
    def normalize():
        ''' normalize filename according to predefined rules

        - extensions shall be in lower case
        '''
        parser = argparse.ArgumentParser(description='scan files into the directory for metadata')
        parser.add_argument('-d', '--directory', dest='path', required=True,
                            help="the path to the directory for file scanning")
        args = parser.parse_args(sys.argv[2:])

        if not os.path.exists(args.path) or not os.path.isdir(args.path):
            parser.print_usage()
            logger.error('The directory does not exist or not directory, {}'.format(args.path))
            sys.exit(1)

        try:
            for filepath in utils.scan_directory(args.path):
                _filepath, _fileext = os.path.splitext(filepath)

                # file extensions shall be in lower case
                _fileext = _fileext.lower()

                # file extensions mapping to common extension formats
                EXT_MAPPING = {
                    '.djv': '.djvu'
                }

                if _fileext in EXT_MAPPING:
                    _fileext = EXT_MAPPING[_fileext]

                _filepath = '{}{}'.format(_filepath, _fileext)
                if filepath != _filepath:
                    logger.info('Rename file, {} to {}'.format(filepath, _filepath))
                    os.rename(filepath, _filepath)
        except KeyboardInterrupt:
            print("Interrupted by user")

    @staticmethod
    def info():
        logger.warning('Not implemented yet')
