
import sys

from filemeta.utils import clean_syspath
sys.path = clean_syspath()

from filemeta.cli import CLI
CLI()

