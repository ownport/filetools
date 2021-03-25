
import os
import logging

from filetools.utils import scan_files
from filetools.libs.tabulate import tabulate


logger = logging.getLogger(__name__)


class Cleaner:

    def __init__(self, path:str) -> None:
        self._path = path

    def use_lower_case_in_file_ext(self, force:bool=False):
        ''' apply rule: use lower case in file extensions
        '''
        try:
            total_files = 0
            total_renamed_files = 0
            total_renamed_files_force = 0

            for filepath in scan_files(self._path):
                total_files += 1
                _filepath, _fileext = os.path.splitext(filepath)
                
                # file extensions shall be in lower case
                _fileext = _fileext.lower()
                _filepath = f'{_filepath}{_fileext}'
                if filepath != _filepath:
                    if os.path.exists(_filepath):
                        if not force:
                            logger.warning(f'Target file path already exists, {filepath} to {_filepath}')
                            continue
                        total_renamed_files_force += 1
                    total_renamed_files += 1
                    os.rename(filepath, _filepath)
            
            print(tabulate(
                (('total files', total_files),
                ('total renamed files', total_renamed_files),
                ('total renamed files (force)', total_renamed_files_force),),
                tablefmt='github'
            ))
            print()
        except KeyboardInterrupt:
            print("Interrupted by user")

    def use_common_file_ext(self, force:bool=False):
        ''' apply rule: use common file extensions
        '''
        try:
            for filepath in scan_files(self._path):
                _filepath, _fileext = os.path.splitext(filepath)

                # file extensions shall be in lower case
                _fileext = _fileext.lower()
                # file extensions mapping to common extension formats
                # EXT_MAPPING = {
                #     '.djv': '.djvu'
                # }

                # if _fileext in EXT_MAPPING:
                #     _fileext = EXT_MAPPING[_fileext]
                _filepath = f'{_filepath}{_fileext}'
                if filepath != _filepath:
                    if os.path.exists(_filepath):
                        if not force:
                            logger.warning(f'Target file path already exists, {filepath} to {_filepath}')
                            continue
                    # os.rename(filepath, _filepath)
        except KeyboardInterrupt:
            print("Interrupted by user")
