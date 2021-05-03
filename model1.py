import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot

# Builtin Imports
import os
import sys
import random

# Custom Imports
import functions


# Retrieve the Current Working Directory and prepare the hard coded stuff
# ----------------------------------------------------------------------------------------
cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
name      = "Agent-Simulator"
inFile    = "in.txt"
outFile   = "out.txt"
storeFile = "store.txt"
# ----------------------------------------------------------------------------------------

# Parse the command line arguments
numAgents, stepIncr, numIterations, neighbourhood, verbose = functions.parseArguments()

# Prepare the file names for IO
inFile    = os.path.join(cwd, "in.txt")
outFile   = os.path.join(cwd, "out.txt")
storeFile = os.path.join(cwd, "store.txt")

# Get the logging object
logger = functions.getLogger(name, cwd, debugToConsole=verbose)
logger.info(f"{name} initialised")
logger.info("Commandline arguments parsed")
logger.info(f"Name: {name}")
logger.info(f"Agents: {numAgents}")
logger.info(f"Agent Step Increment: {stepIncr}")
logger.info(f"Iterations: {numIterations}")
logger.info(f"Neighbourhood: {neighbourhood}")
logger.info(f"Verbosity: {verbose}")
logger.info(f"Environment File: {inFile}")
logger.info(f"Environment Result: {outFile}")
logger.info(f"Store File: {storeFile}")

# Load the environment raster and discover the x & y limits
environment = functions.loadEnvFromCSV(inFile)
xLim = len(environment[0])
yLim = len(environment)

# Quick Configs for testing. Commented out when not needed
#-----------------------------------------------------------------------------------------
numAgents = 50
stepIncr = 1
numIterations = 0
neighbourhood = 20
verbose = True
#-----------------------------------------------------------------------------------------

#sys.exit()

# Create the agents.
agents = []
logger.info("Creating agents.")
functions.createAgents(environment, xLim, yLim, numAgents, agents)
logger.info(f"Done. There are {len(agents)} agents.")

# Delete the store file if exists.
if os.path.isfile(storeFile):
    os.remove(storeFile)
    logger.info(f"Store file {storeFile} deleted")


fig, ax = matplotlib.pyplot.subplots()
matplotlib.pyplot.xlim(0, xLim)
matplotlib.pyplot.ylim(0, yLim)
sc = ax.scatter(0, 0, marker=".", c="Black")

# We only need to show the image once, then update the data. Otherwise, performance degrades
image = matplotlib.pyplot.imshow(environment)

def animate(i):
    xy = []
    totalStore = 0
    random.shuffle(agents)
    #Possibly update data only every x frames
    image.set_data(environment)
    for agent in agents:
        agent.move()
        agent.eat()
        agent.shareWithNeighbours(neighbourhood)
        totalStore += agent.store
        xy.append([agent.x, agent.y])

    # Add more agents
    # --------------------------------------------------------------------------------
    if 0 < stepIncr <= 20:
        #logger.info(f"Adding {stepIncr} more agents.")
        functions.createAgents(environment, xLim, yLim, stepIncr, agents)
        #logger.info("Done.")
        print(len(agents))


    with open(storeFile, "at") as oStore:
        oStore.write(f"{totalStore}\n")


    sc.set_offsets(xy)


ani = matplotlib.animation.FuncAnimation(fig, animate, frames=50, interval=1, repeat=True)
matplotlib.pyplot.show()



functions.saveEnvToCSV(environment, outFile)





























