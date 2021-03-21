
import os
import sys
import json
import logging
import argparse

from collections import Counter

from filetools import utils
from filetools.scanner import Scanner
from filetools.version import version


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
        parser.add_argument('-d', '--directory', dest='path', required=True,
                            help="the path to the directory for file scanning")
        args = parser.parse_args(sys.argv[2:])

        if not os.path.exists(args.path) or not os.path.isdir(args.path):
            parser.print_usage()
            logger.error('The directory does not exist or not directory, {}'.format(args.path))
            sys.exit(1)

        try:
            files = Counter()
            extensions = Counter()
            for filepath in utils.scan_directory(args.path):
                files['total_files'] += 1
                extensions[os.path.splitext(filepath)[1]] += 1

            result = dict(files)
            result['extensions'] = dict(extensions)
            print(json.dumps(result))
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
