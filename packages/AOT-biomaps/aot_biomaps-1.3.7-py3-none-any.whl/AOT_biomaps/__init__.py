from .AOT_Acoustic import *
from .AOT_Optic import *
from .AOT_AOsignal import *
from .config import config

__version__ = '1.3.7'


def initialize(process='cpu'):
    config.set_process(process)
    print(f"Initialized with process: {config.get_process()}")