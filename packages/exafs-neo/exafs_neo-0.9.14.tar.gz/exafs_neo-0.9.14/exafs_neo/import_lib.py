# Import Library
from .helper import *
from .import_lib import *
from .input_arg import *

if timeing_mode:
    t1 = timecall()

from psutil import cpu_count
# Set the number of threads
import os

os.environ['NUMEXPR_MAX_THREADS'] = str(cpu_count())
import larch

larch_version = larch.__version__.split('.')
try:
    from larch import Interpreter
    from larch.io import read_ascii
    from larch.xafs import autobk, feffdat, xftf
except:
    from larch_plugins.io import read_ascii
    from larch_plugins.xafs import autobk
    from larch_plugins.xafs import feffdat
    from larch_plugins.xafs import xftf

# from multiprocessing import Pool
# import multiprocessing as mp
# import ray
# from multiprocessing import Pool as ProcessPool
# from multiprocessing.dummy import Pool as ThreadPool  ### this uses threads


if timeing_mode:
    initial_elapsed = timecall() - t1
    print('Inital import function took %.2f second' % initial_elapsed)
