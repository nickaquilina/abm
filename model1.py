# Builtin Imports
import os
import sys
import csv
import time
import random
import argparse
import shutil
import logging
import logging.handlers
import traceback
# Other Imports
import matplotlib.pyplot
# Custom Imports
import agentframework


# Retrieve the Current Working Directory and prepare the configurables
# ----------------------------------------------------------------------------------------
cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
name      = "Agent-Simulator"
inFile    = "in.txt"
outFile   = "out.txt"
storeFile = "store.txt"


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

    parser.add_argument("-a", dest="numAgents", default=10,
                        help='The number of Agents to spawn. Default is 10.')

    parser.add_argument("-s", dest="agentStepIncr", default=0,
                        help='Increments the Agents by this value on each run.')

    parser.add_argument("-i", dest="numIterations", default=100,
                        help="Iterations to run through. Default is 100")

    parser.add_argument("-n", dest="neighbourhood", default=20,
                        help="Neighbourhood distance. Default is 20")

    parser.add_argument("-v", dest="verbose", action="store_true",
                        help="Use this switch to enable debug logging to the console.")

    args = parser.parse_args()

    try:
        numAgents = int(args.numAgents)
        agentStepIncr = int(args.agentStepIncr)
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
        agentStepIncr = defaults["agentStepIncr"]
        numIterations = defaults["numIterations"]
        neighbourhood = defaults["neighbourhood"]
    finally:
        verbose = args.verbose
        return numAgents, agentStepIncr, numIterations, neighbourhood, verbose



def loadEnvFromCSV(f):
    """ Load the raster data from the Comma Seperated Values file
    """
    environment = []

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


# Parse the command line arguments
numAgents, agentStepIncr, numIterations, neighbourhood, verbose = parseArguments()

# Prepare the file names for IO
inFile    = os.path.join(cwd, "in.txt")
outFile   = os.path.join(cwd, "out.txt")
storeFile = os.path.join(cwd, "store.txt")

# Get the logging object
logger = getLogger(name, cwd, debugToConsole=verbose)
logger.info(f"{name} initialised")
logger.info("Commandline arguments parsed")

logger.info(f"Name: {name}")
logger.info(f"Agents: {numAgents}")
logger.info(f"Agent Step Increment: {agentStepIncr}")
logger.info(f"Iterations: {numIterations}")
logger.info(f"Neighbourhood: {neighbourhood}")
logger.info(f"Verbosity: {verbose}")

logger.info(f"Environment File: {inFile}")
logger.info(f"Environment Result: {outFile}")
logger.info(f"Store File: {storeFile}")


# Load the environment raster and discover the x & y limits
environment = loadEnvFromCSV(inFile)
xLim = len(environment[0])
yLim = len(environment)


# Create the agents.
agents = []
logger.info("Creating agents.")
for n in range(numAgents):
    agents.append(agentframework.Agent(environment, xLim, yLim, agents))
logger.info(f"Done. There are {len(agents)} agents.")



# Delete the store file if exists.
if os.path.isfile(storeFile):
    os.remove(storeFile)
    logger.info(f"Store file {storeFile} deleted")

# Move the agents.
first = True
for j in range(numIterations):
    logger.info(f"Iteration: {j+1}")
    """ Increment the number of agents if the agentStepIncr variable is greater than 0. A
        A limit of 20 is hardcoded for now, since adding a lot of agents can lead to
        performance problems
    """
    if (0 < agentStepIncr <= 20) and not first:
        logger.info("Adding more agents.")
        for n in range(agentStepIncr):
            agents.append(agentframework.Agent(environment, xLim, yLim, agents))
        logger.info(f"Done. There are {len(agents)} agents.")
    first = False

    #-------------------------------------------------------------------------------------
    """
    if j % int(numIterations/10) == 0:
        logger.info(f"Iteration: {j}")
    """

    totalStore = 0
    random.shuffle(agents)

    for i in range(numAgents):
        #print(f"Agent: {i} - id:{id(agents[i])}")
        agents[i].move()
        agents[i].eat()
        agents[i].shareWithNeighbours(neighbourhood)

        totalStore += agents[i].store

    with open(storeFile, "at") as oStore:
        oStore.write(f"{totalStore}\n")



logger.info(f"Done. {numIterations} iterations executed.")


matplotlib.pyplot.xlim(0, xLim)
matplotlib.pyplot.ylim(0, yLim)

matplotlib.pyplot.imshow(environment)
for i in range(len(agents)):
    matplotlib.pyplot.scatter(agents[i].x,agents[i].y, marker=".")
matplotlib.pyplot.show()


saveEnvToCSV(environment, outFile)
















