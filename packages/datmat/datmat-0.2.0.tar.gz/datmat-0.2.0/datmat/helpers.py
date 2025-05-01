from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path

from .typehints import pathlike


def copy_file_dir(inpath: pathlike,
                  outpath: pathlike):
    """
    Helper function, copies a file or directory not caring what the inpath
    actually is

    :param inpath: path of the things to be copied
    :param outpath: path of the destination
    :return: the result of shutil.copy2 or shutil.copytree (depending on
             inpath pointing to a file or directory)
    """
    if os.path.isfile(inpath):
        if os.path.exists(outpath):
            remove_file_dir(outpath)
        return shutil.copy2(inpath, outpath)
    elif os.path.isdir(inpath):
        if os.path.exists(outpath):
            remove_file_dir(outpath)
        return shutil.copytree(inpath, outpath, symlinks=True)
    else:
        raise ValueError('Cannot copy {}, not a valid file or directory!'.format(inpath))


def link_or_copy(source: pathlike,
                 destination: pathlike):
    try:
        os.symlink(source, destination)
    except OSError:
        shutil.copy2(source, destination)


def remove_file_dir(inpath: pathlike):
    inpath = Path(inpath)
    if inpath.exists() and inpath.is_symlink():
        inpath.unlink()
    elif inpath.exists() and inpath.is_file():
        os.remove(inpath)
    elif inpath.exists() and inpath.is_dir():
        shutil.rmtree(inpath) 
    else:
        raise ValueError('Cannot remove {}, not a valid file or directory!'.format(inpath))


def create_logger(*, debug: bool = False, loglevel: str = 'INFO') -> logging.Logger:
    logger = logging.getLogger('data-materialisation')
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        # create formatter
        if debug:
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(module)s:%(lineno)d >> %(message)s')
        else:
            formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)

    if loglevel is not None:
        logger.setLevel(loglevel)
    elif debug:
        logger.setLevel('DEBUG')
    else:
        logger.setLevel('WARNING')

    return logger
