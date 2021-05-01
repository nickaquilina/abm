import os
import csv
import traceback
import matplotlib.pyplot
import agentframework

def distance_between(agents_row_a, agents_row_b):
    return (((agents_row_a.x - agents_row_b.x)**2) +
    ((agents_row_a.y - agents_row_b.y)**2))**0.5


def csvFileReader(f):
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


def csvFileWriter(data, csvFile):
    """ Function to write CSV data back to a CSV file. No need to delete the
        file prior to writing, since I amopening in write mode not append.
    """
    with open(csvFile, "wt", newline="") as openFile:
        csvWriter = csv.writer(openFile)
        for item in data:
            csvWriter.writerow(item)





num_of_agents = 1000
num_of_iterations = 1000
agents = []


# Load the CSV Data and create the environment var
# -----------------------------------------------------------------------------
fl = os.path.join(os.getcwd(), "in.txt")
environment = csvFileReader(fl)
xLim = len(environment[0])
yLim = len(environment)


# Make the agents.
for i in range(num_of_agents):
    agents.append(agentframework.Agent(environment, xLim, yLim))


# Delete the store file if exists. COuld have simply opened in Write mode first
# time instead, but this is cleaner.
storeFile = os.path.join(os.getcwd(), "store.txt")
if os.path.isfile(storeFile):
    os.remove(storeFile)

# Move the agents.
for j in range(num_of_iterations):
    print(f"Iteration: {j}")
    totalStore = 0
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        ###print(agents[i].store)
        totalStore += agents[i].store
    ###print(f"Total Store: {totalStore}")
    with open(storeFile, "at") as oStore:
        oStore.write(f"{totalStore}\n")


matplotlib.pyplot.xlim(0, xLim)
matplotlib.pyplot.ylim(0, yLim)

matplotlib.pyplot.imshow(environment)
for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i].x,agents[i].y, marker=".")
matplotlib.pyplot.show()

outFile = os.path.join(os.getcwd(), "out.txt")
csvFileWriter(environment, outFile)


"""
for agents_row_a in agents:
    for agents_row_b in agents:
        distance = distance_between(agents_row_a, agents_row_b)
        print(distance)
"""


"""
for agent in agents:
    print(agent.getCoordinates())
    agent.move()
    print(agent.getCoordinates())
    print("-----------------------------")
"""






















