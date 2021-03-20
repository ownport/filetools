
import os
import sys

from filetools.utils import filehash
from filetools.utils import get_tags_from_path
from filetools.utils import scan_directory


def test_utils_filehash_absent_file():
    ''' test for calculation sha256 hash for absent file
    '''
    assert filehash('absent_file') is None

def test_utils_filehash(request):
    ''' test for calculation sha256 hash for file
    '''
    filepath = os.path.join(request.fspath.dirname, 'resources', 'test_file.1')
    assert filehash(filepath) == 'e210ef9246993b64e815b23abfed49598260988bec108c2975406c20a7839b20'

def test_utils_get_tags_from_path(request):
    ''' test for getting tags from a path
    '''
    filepath = os.path.join(request.fspath.dirname, 'resources', 'test_file.1')
    tags = get_tags_from_path(filepath)
    assert 'tests' in tags
    assert 'resources' in tags
    assert 'filetools' in tags

def test_utils_get_tags_from_path_with_prefix(request):
    ''' test for getting tags from a path with prefix
    '''
    filepath = os.path.join(request.fspath.dirname, 'resources', 'test_file.1')
    tags = get_tags_from_path(filepath, prefix='filetools')
    assert 'tests' in tags
    assert 'resources' in tags
    assert 'filetools' not in tags

def test_utils_get_tags_from_path_with_ignore_tags(request):
    ''' test for getting tags from a path with ignore tags
    '''
    filepath = os.path.join(request.fspath.dirname, 'resources', 'test_file.1')
    tags = get_tags_from_path(filepath, ignore_tags=['tests', 'resources'])
    assert 'tests' not in tags
    assert 'resources' not in tags
    assert 'filetools' in tags

def test_utils_scan_directory(request):
    ''' test for directory scan
    '''
    path = os.path.join(request.fspath.dirname, 'resources')
    files = list(scan_directory(path))
    assert files == [
    ]
