from . import utils as F
from . import logger as Log
from . import sync as S

def globalInitialize(source, replica, log_path, interval):
    Log.initialize_logger(log_path)
    F.verifyPaths(source, replica, log_path)
    S.initialize(source, replica, interval)
