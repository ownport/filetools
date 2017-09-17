
import sys

from filetools.utils import clean_syspath
sys.path = clean_syspath()

from filetools.cli import CLI
CLI()

