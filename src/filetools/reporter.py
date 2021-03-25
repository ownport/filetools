
import os
import logging

from typing import DefaultDict

from filetools.utils import scan_files
from filetools.utils import convert_size
from filetools.libs.tabulate import tabulate

logger = logging.getLogger(__name__)


class Reporter:

    def __init__(self, path:str) -> None:
        self._path = path

    def print_general_stats(self):
        ''' print general statistics
        '''
        total_files = 0
        total_directories = 0
        total_empty_files = 0
        total_empty_directories = 0
        try:
            for root, _, files in os.walk(self._path):
                total_files  += len(files)
                total_directories += 1
                total_empty_files += sum([1 for file in files if os.stat(os.path.join(root, file)).st_size == 0])
                if len(files) == 0:
                    total_empty_directories =+ 1

            print("\nGeneral statistics:\n")
            print(tabulate(
                    (('Total files', total_files),
                    ('Total directories', total_directories),
                    ('Total empty files', total_empty_files),
                    ('Total empty directories', total_empty_directories)),
                    headers=('Metric', 'Value'),
                    tablefmt="github")
            )
        except KeyboardInterrupt:
            print("Interrupted by user")

    def print_file_extension_stats(self, sort_by:str='size') -> None:
        ''' print file extension stats
        '''
        try:
            stats = DefaultDict(lambda: DefaultDict(int))
            for filepath in scan_files(self._path):
                ext = os.path.splitext(filepath)[1]
                stats[ext]['files'] += 1
                try:
                    stats[ext]['size'] += os.stat(filepath).st_size
                except (OSError, FileNotFoundError) as err:
                    logger.warning(err)

            data = [(ext, info['files'], info['size'] ) for ext, info in stats.items()]
            sorting_field_id = 1 if sort_by == 'files' else 2 # if by size
            data = sorted(data, key=lambda x: x[sorting_field_id], reverse=True)
            data = [(ext, files, convert_size(size)) for ext, files, size in data]
            print("\nFile Extensions statistics:\n")
            print(tabulate(
                    data, 
                    headers=['Extension', "Files", "Size"], 
                    tablefmt="github")
            )
        except KeyboardInterrupt:
            print("Interrupted by user")
