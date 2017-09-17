
import os
import re
import sys
import hashlib
import logging

logger = logging.getLogger(__name__)

def clean_syspath():
    ''' Cleaner removes from sys.path any external libs to avoid potential
    # conflicts with existing system libraries

    :return: updated sys.path
    '''
    result = []
    for p in sys.path:
        if p.endswith('site-packages'):
            continue
        if p.endswith('dist-packages'):
            continue
        if p.endswith('lib-old'):
            continue
        if p.endswith('lib-tk'):
            continue
        if p.endswith('gtk-2.0'):
            continue
        result.append(p)
    return result


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


def scan_directory(path):
    ''' scan directory
    '''
    logger.info('The scanning was started,: {}'.format(path))
    for root, dirs, files in os.walk(path):
        if not files:
            continue
        for filename in files:
            filepath = os.path.join(root, filename)
            yield filepath
    logger.info('The scaning was completed successfully')


def get_meta(filepath, ignore_tags=[]):
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
