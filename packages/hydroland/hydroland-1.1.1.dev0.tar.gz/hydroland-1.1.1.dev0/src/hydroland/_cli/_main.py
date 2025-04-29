import logging
import sys

from hydroland.completion import cleanup_files
from hydroland.completion import parse_args as parse_args_cleanup_files
from hydroland.initialisation import parse_args as parse_args_initialisation
from hydroland.initialisation import start_initialisation
from hydroland.mhm import execute_mhm
from hydroland.mhm import parse_args as parse_args_execute_mhm
from hydroland.mrm import execute_mrm
from hydroland.mrm import parse_args as parse_args_execute_mrm
from hydroland.preprocessing import parse_args as parse_args_prepare_forcings
from hydroland.preprocessing import preprocess_forcings


def _cli_logger():
    # grab (or create) your "hydroland" logger
    logger = logging.getLogger("hydroland")
    logger.setLevel(logging.INFO)

    # create a stream handler that writes to stdout
    sh = logging.StreamHandler(sys.stdout)

    # give it the same format and datefmt you had in basicConfig
    fmt = "%(asctime)s %(name)s %(levelname)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    sh.setFormatter(formatter)

    # (optionally) avoid adding multiple handlers on repeated calls
    if not logger.handlers:
        logger.addHandler(sh)

    return logger


def initialize(argv=None):
    """
    Execute map CLI routine.

    Parameters
    ----------
    argv : list of str
        command line arguments, default is None

    Returns
    -------

    """
    _cli_logger()
    args = parse_args_initialisation(argv)
    start_initialisation(**vars(args))


def prepare_forcings(argv=None):
    """
    Execute map CLI routine.

    Parameters
    ----------
    argv : list of str
        command line arguments, default is None

    Returns
    -------

    """
    _cli_logger()
    args = parse_args_prepare_forcings(argv)
    preprocess_forcings(**vars(args))


def run_mhm(argv=None):
    """
    Execute map CLI routine.

    Parameters
    ----------
    argv : list of str
        command line arguments, default is None

    Returns
    -------

    """
    _cli_logger()
    args = parse_args_execute_mhm(argv)
    execute_mhm(**vars(args))


def run_mrm(argv=None):
    """
    Execute estimate CLI routine.

    Parameters
    ----------
    argv : list of str
        command line arguments, default is None

    Returns
    -------

    """
    _cli_logger()
    args = parse_args_execute_mrm(argv)
    execute_mrm(**vars(args))


def conclude(argv=None):
    """
    Execute estimate CLI routine.

    Parameters
    ----------
    argv : list of str
        command line arguments, default is None

    Returns
    -------

    """
    _cli_logger()
    args = parse_args_cleanup_files(argv)
    cleanup_files(**vars(args))
