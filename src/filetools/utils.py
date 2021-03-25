
import os
import re
import math
import hashlib
import logging
import pathlib

from typing import Generator

logger = logging.getLogger(__name__)


def filehash(path):
    ''' return sha256 hash for specified path
    '''
    if os.path.exists(path):
        _filehash = hashlib.sha256()
        with open(path, 'rb') as reader:
            while True:
                chunk = reader.read(64000)
                if not chunk:
                    break
                _filehash.update(chunk)
            return _filehash.hexdigest()

    return None


def get_tags_from_path(path, prefix=None, ignore_tags=list()):
    ''' return tags list from path
    '''
    if prefix:
        path = path.replace(prefix, '')

    result = []
    if ignore_tags:
        ignore_tags = [re.compile(p) for p in ignore_tags]
        result.extend([t for t in path.split(os.sep)[:-1]
                if t and sum(map(lambda x: 1 if x.match(t) else 0, ignore_tags)) == 0])
    else:
        result.extend([t for t in path.split(os.sep)[:-1] if t])
    return list(set(result))


def scan_files(path:str, remove_root_path:bool=False) -> Generator:
    ''' scan files in directory
    '''
    for root, _, files in os.walk(path):
        if not files:
            continue
        for filename in files:
            filepath = os.path.join(root, filename)
            if remove_root_path:
                filepath = filepath.replace(path, '')
            yield filepath

def get_meta(filepath, ignore_tags=()):
    ''' return meta by filepath
    '''
    return {
        'sha256': filehash(filepath),
        'path': filepath,
        'name': filepath.split(os.sep)[-1],
        'ext': os.path.splitext(filepath)[1],
        'size': os.stat(filepath).st_size,
        'tags': get_tags_from_path(filepath, ignore_tags=ignore_tags),
    }


def pairtree_path(filehash, level=2):
    ''' return pairtree path based on the level of depth
    '''
    parts = [filehash[(i*2):(i*2)+2] for i,l in enumerate(range(level))]
    parts.append(filehash)
    return os.sep.join(parts)


def convert_size(size_bytes:int) -> str:
    ''' convert size in bytes to string in human readable format
    '''
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def progress_bar (iteration:int, total:int, 
                    prefix:str = 'Progress:', suffix:str = 'Completed',
                    decimals:int = 1, length:int = 50, 
                    fill:str = '#', print_end:str = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end    - Optional  : end character (e.g. "\r", "\r\n") (Str)

    Sample of usage    
    ------------------
    ```
    import time

    # A List of Items
    items = list(range(0, 57))
    l = len(items)

    # Initial call to print 0% progress
    progress_bar(0, l)
    for i, item in enumerate(items):
        # Do stuff...
        time.sleep(0.1)
        # Update Progress Bar
        printProgressBar(i + 1, l)
    ```
    original link: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} [{bar}] {percent}% {suffix}', end = print_end)

