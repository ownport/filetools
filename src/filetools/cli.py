
import os
import sys
import json
import logging
import argparse


from filetools import FILEMETA_VERSION
from filetools import utils


FILEMETA_USAGE = '''filemeta <command> [<args>]
The list of commands:
    scan    scan files into the directory for metadata           
    info    collect metedata from the file        
'''

logger = logging.getLogger(__name__)


class CLI():

    def __init__(self):
        parser = argparse.ArgumentParser(usage=FILEMETA_USAGE)
        parser.add_argument('-v', '--version', action='version',
                            version='filemeta-v{}'.format(FILEMETA_VERSION))
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
        parser = argparse.ArgumentParser(description='scan files into the directory for metadata')
        parser.add_argument('-d', '--directory', dest='path', required=True,
                            help="the path to the directory for file scanning")
        parser.add_argument('-i', '--ignore-tags', action='append',
                            help='the tags for ignoring')
        args = parser.parse_args(sys.argv[2:])

        if not os.path.exists(args.path) or not os.path.isdir(args.path):
            parser.print_usage()
            logger.error('The directory does not exist or not directory, {}'.format(args.path))
            sys.exit(1)

        for filepath in utils.scan_directory(args.path):
            logger.info('Processing the file, {}'.format(filepath))
            print(json.dumps(utils.get_meta(filepath, ignore_tags=args.ignore_tags)))

    @staticmethod
    def info():
        pass
