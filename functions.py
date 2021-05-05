""" This file contains all the functions used by the model script. Moved here for cleaner
    main file.
"""
import os
import sys
import csv
import time
import shutil
import logging
import argparse
import traceback
import logging.handlers

import agentframework


def getLogger(name, cwd, debugToConsole=False):
    """ A basic logging function. Since the script generates a lot of debug information,
        rather than using the inefficient print function, I implemented simple logging,
        where a logging object is acquired at the beginning and used throughout.

        Info produces only minimal logging just to ensure all is ok, while the debug
        writes copious amounts of data to a different log file.

        Writing to the console is also parametrised, in that, by default, only info is
        sent to the console (as well) Debug to console should only be used with smallish
        runs, since it negatively affects performance.
    """
    logsToKeep = 5
    logBytes = 5242880 # 5Mb * 1048576 bytes

    debugFile = os.path.join(cwd, f"{name}.debug.log")
    infoFile = os.path.join(cwd, f"{name}.info.log")

    # Instead of deleting old log files, I am renaming uwing a timestamp. This ensures old
    # log files are stored for posterity, while at the same making log viewing easier
    # since only data for the current run is present.
    listing = os.listdir(cwd)
    for item in listing:
        if ("debug.log" in item or "info.log" in item) and "backup" not in item:
            try:
                sourcePath = os.path.join(cwd, item)
                newName = f"{int(time.time())}_backup_{item}"
                destPath = os.path.join(cwd, "debuglogsarchive", newName)
                shutil.move(sourcePath, destPath)
            except PermissionError:
                print(f"Cannot delete {sourcePath}")
                print(traceback.format_exc())


    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    msgFormat = "%(asctime)s %(levelname)-8s : %(module)-10s Ln:%(lineno)4d : %(message)s"
    formatter = logging.Formatter(msgFormat)

    # Console Handler

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    if debugToConsole:
        consoleHandler.setLevel(logging.DEBUG)
    else:
        consoleHandler.setLevel(logging.INFO)
    logger.addHandler(consoleHandler)

    debugHandler = logging.handlers.RotatingFileHandler(debugFile, maxBytes=logBytes,\
                                                        backupCount = logsToKeep)

    debugHandler.setFormatter(formatter)
    debugHandler.setLevel(logging.DEBUG)
    logger.addHandler(debugHandler)

    infoHandler = logging.handlers.RotatingFileHandler(infoFile, maxBytes=logBytes, \
                                                       backupCount = logsToKeep)
    infoHandler.setFormatter(formatter)
    infoHandler.setLevel(logging.INFO)
    logger.addHandler(infoHandler)

    return logger


def parseArguments():
    print(f"ARGV Length: {len(sys.argv)}")
    if len(sys.argv) > 10:
        # Using print here, since the logger is not yet avaialble
        print("Too many arguments. Run the program with -h for help")
        print("Exiting")
        sys.exit()

    parser = argparse.ArgumentParser(description="Agent Simulator. Random agents \
                                                  interacting with the environment and \
                                                  each other.")

    parser.add_argument("-a", dest="numAgents", default=20,
                        help='The number of Agents to spawn. Default is 10.')

    parser.add_argument("-s", dest="stepIncr", default=0,
                        help='Increments the Agents by this value on each run.')

    parser.add_argument("-i", dest="numIterations", default=500,
                        help="Iterations to run through. Default is 100")

    parser.add_argument("-n", dest="neighbourhood", default=20,
                        help="Neighbourhood distance. Default is 20")

    parser.add_argument("-v", dest="verbose", action="store_true",
                        help="Use this switch to enable debug logging to the console.")

    args = parser.parse_args()

    try:
        numAgents = int(args.numAgents)
        stepIncr = int(args.stepIncr)
        numIterations = int(args.numIterations)
        neighbourhood = int(args.neighbourhood)
    except ValueError:
        print("Values need to be integers")
        print("Proceeding with the default variables")
        print(traceback.format_exc())

        defaults = {}
        for key in vars(args):
            defaults[key] = parser.get_default(key)

        numAgents = defaults["numAgents"]
        stepIncr = defaults["stepIncr"]
        numIterations = defaults["numIterations"]
        neighbourhood = defaults["neighbourhood"]
    finally:
        verbose = args.verbose
        return numAgents, stepIncr, numIterations, neighbourhood, verbose


def createAgents(env, xL, yL, amount, aList, logger):
    for i in range(amount):
        aList.append(agentframework.Agent(env, xL, yL, aList, logger))


def loadEnvFromCSV(f):
    """ Load the raster data from the Comma Seperated Values file
    """
    environment = []
    print(f)
    try:
        with open(f, "r") as openFile:
            dataReader = csv.reader(openFile)
            for row in dataReader:
                rowlist = []
                for col in row:
                    rowlist.append(int(col))
                environment.append(rowlist)

    except FileNotFoundError:
        print(f"File not found: {f}")
        print(traceback.format_exc())
        environment = None

    return environment


def saveEnvToCSV(data, csvFile):
    """ Function to write CSV data back to a CSV file. No need to delete the
        file prior to writing, since I amopening in write mode not append.
    """
    with open(csvFile, "wt", newline="") as openFile:
        csvWriter = csv.writer(openFile)
        for item in data:
            csvWriter.writerow(item)













