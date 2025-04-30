#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from logging import handlers
import os

level_relations = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}


def getconsolelogger(name, param_format='%(message)s', level=logging.INFO):
    """
    Return a console logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    console = logging.StreamHandler()
    logger.addHandler(console)
    formatter = logging.Formatter(param_format)
    console.setFormatter(formatter)
    return logger


def getfilelogger(name, file, param_format='%(message)s', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    garder = os.path.dirname(file)
    if not os.path.exists(garder):
        os.makedirs(garder)
    filehandle = logging.FileHandler(file)
    logger.addHandler(filehandle)
    formatter = logging.Formatter(param_format)
    filehandle.setFormatter(formatter)
    return logger


def getthfilelogger(name, file, log_format='%(message)s', level="info", when="D", interval=1, back_count=1000):
    logger = logging.getLogger(name)
    logger.setLevel(level_relations.get(level))
    th = handlers.TimedRotatingFileHandler(filename=file,
                                           when=when,
                                           backupCount=back_count,
                                           interval=interval,
                                           encoding="utf-8")
    logger.addHandler(th)
    formatter = logging.Formatter(log_format)
    th.setFormatter(formatter)
    return logger


def getbuflogger(name, file, log_format='%(message)s', level="info", log_mode="a", log_max_bytes=1024000, bk_count=100):
    logger = logging.getLogger(name)
    logger.setLevel(level_relations.get(level))
    th = handlers.RotatingFileHandler(filename=file,
                                      mode=log_mode,
                                      maxBytes=log_max_bytes,
                                      backupCount=bk_count,
                                      encoding="utf-8",
                                      delay=False)
    logger.addHandler(th)
    formatter = logging.Formatter(log_format)
    th.setFormatter(formatter)
    return logger


def logshutdown():
    logging.shutdown()


def close(log: logging.Logger):
    for h in log.handlers:
        if h:
            try:
                h.acquire()
                h.flush()
                h.close()
            except (OSError, ValueError):
                # Ignore errors which might be caused
                # because handlers have been closed but
                # references to them are still around at
                # application exit.
                pass
            finally:
                h.release()
