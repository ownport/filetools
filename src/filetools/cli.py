
import os
import sys
import logging
import argparse

from typing import DefaultDict

from filetools import utils
from filetools.cleaner import Cleaner
from filetools.scanner import Scanner
from filetools.version import version
from filetools.utils import convert_size
from filetools.libs.tabulate import tabulate


FILETOOLS_USAGE = '''filetools <command> [<args>]
The list of commands:
    stats       collect statistics about files in the directory
    scan        scan files into the directory for metadata           
    cleanup     removing files, renaming
    info        collect metedata from the file        
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
        parser = argparse.ArgumentParser(description='scan files into the directory for metadata')
        parser.add_argument('--path', dest='path', required=True,
                            help="the path to the directory for file scanning")
        parser.add_argument('--output-type', dest='output_type',
                            choices=['jsonline', 'sqlite3'],
                            help="the output type")
        parser.add_argument('--output-file', dest='output_file',
                            help="the path output file for storing metadata")
        parser.add_argument('--ignore-tag', dest='ignore_tags', action='append',
                            help='the tags for ignoring')
        _args = parser.parse_args(sys.argv[2:])

        try:
            scanner = Scanner(_args.path, _args.output_type, _args.output_file, _args.ignore_tags)
            scanner.scan_files()
            scanner.close()
        except Exception as err:
            logger.error(err)

    @staticmethod
    def stats():
        ''' scan directory for collection general stats about files
        '''
        parser = argparse.ArgumentParser(description='scan files into the directory for metadata')
        parser.add_argument('--path', dest='path', required=True,
                            help="the path to the directory for file scanning")
        parser.add_argument('--sort-by', dest='sort_by', default='size',
                            choices=['files', 'size'],
                            help="sort output by number or files or size, default: size")
        args = parser.parse_args(sys.argv[2:])

        if not os.path.exists(args.path) or not os.path.isdir(args.path):
            parser.print_usage()
            logger.error('The directory does not exist or not directory, {}'.format(args.path))
            sys.exit(1)

        try:
            files = 0
            stats = DefaultDict(lambda: DefaultDict(int))
            for filepath in utils.scan_files(args.path):
                files  += 1
                ext = os.path.splitext(filepath)[1]
                stats[ext]['files'] += 1
                try:
                    stats[ext]['size'] += os.stat(filepath).st_size
                except (OSError, FileNotFoundError) as err:
                    logger.warning(err)

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
    def cleanup():
        ''' cleanup filenames according to predefined rules

        Rules:
        - extensions shall be in lower case
        '''
        parser = argparse.ArgumentParser(description='scan files into the directory for metadata')
        parser.add_argument('--path', dest='path', required=True,
                            help="the path to the directory for file scanning")
        parser.add_argument('--use-lower-case-in-file-ext', action='store_true', default=False,  
                            help="use lower case in file extensions, default: False")
        parser.add_argument('--remove-broken-files', action='store_true', default=False,  
                            help="remove broken-files")
        parser.add_argument('--force', action='store_true', default=False,  
                            help="apply forced action, default: False")
        args = parser.parse_args(sys.argv[2:])

        if not os.path.exists(args.path) or not os.path.isdir(args.path):
            parser.print_usage()
            logger.error('The directory does not exist or not directory, {}'.format(args.path))
            sys.exit(1)

        cleaner = Cleaner(args.path)
        if args.use_lower_case_in_file_ext:
            cleaner.use_lower_case_in_file_ext(args.force)
        if args.remove_broken_files:
            cleaner.remove_broken_files(args.force)
        

    @staticmethod
    def info():
        logger.warning('Not implemented yet')
