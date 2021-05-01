""" @author: Nicholas Aquilina
    Lightweight library for debug logging.
"""

import os
import sys
import logging
import logging.handlers


def getLogger(name, cwd, log_size_mb=5, logsToKeep=5, writeInfoLog=False):
    # Convert the Megabytes to bytes
    log_size_bytes = log_size_mb * 1048576

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    msg_format = "%(asctime)s %(levelname)-8s : %(module)-26s Ln:%(lineno)4d : %(message)s"
    logMsgFormat = logging.Formatter(msg_format)

    # Set the console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logMsgFormat)
    consoleHandler.setLevel(logging.DEBUG)
    logger.addHandler(consoleHandler)

    # Debug handler
    debugLogFile = os.path.join(cwd, f"{name}.debug.log")
    f = open(debugLogFile, "a")
    f.close()
    debugHandler = logging.handlers.RotatingFileHandler(debugLogFile,
                                                        maxBytes=log_size_bytes,
                                                        backupCount = logsToKeep)
    debugHandler.setFormatter(logMsgFormat)
    debugHandler.setLevel(logging.DEBUG)
    logger.addHandler(debugHandler)


    # INFO file and Handler. Optional
    if writeInfoLog:
        infoLogFile = os.path.join(cwd, f"{name}.info.log")
        f = open(infoLogFile, "a")
        f.close()

        infoHandler = logging.handlers.RotatingFileHandler(infoLogFile, maxBytes = log_size_bytes, backupCount = logsToKeep)
        infoHandler.setFormatter(logMsgFormat)
        infoHandler.setLevel(logging.INFO)
        logger.addHandler(infoHandler)

    return logger


def validate_log_dir(d):
    """ Function takes care of validating the logging directory. If the directory is not present, it
        will try to first create the directory. If something breaks in the process, the function
        returns a False, so that the logging library then does not create the rotating file handler
        and instead, simply writes logging to stdout.
    """



n = "Test Logger"
cwd = os.path.dirname(os.path.abspath(sys.argv[0]))

l = getLogger(n, cwd, writeInfoLog=True)

l.debug("Muhahaha")

