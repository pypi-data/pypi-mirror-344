from .AOT_Acoustic import *
from .AOT_Optic import *
from .AOT_AOsignal import *
from .config import config

__version__ = '1.4.4'

if config.get_process() == 'gpu':
    __process__ = 'gpu'
else:
    __process__ = 'cpu'

def initialize(process='cpu'):
    config.set_process(process)
    print(f"Initialized with process: {config.get_process()}")

