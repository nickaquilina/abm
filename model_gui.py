import matplotlib
matplotlib.use('TkAgg')
import os
import sys
import time
import tkinter
import requests
import threading
import traceback
from lxml import etree
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Custom Imports
import functions
import agentframework


# Get the current working directory. This makes it easy to build paths, and in general
# stay within the folder "context" the name is at this point only used for the logger
# instance.
# ----------------------------------------------------------------------------------------
# Debug logging is always written to the debug logs stored at the root of the Model script
# This is simply to enable/disable showing extended logging in the console, which should
# not even be required. This procures a large amout of logging, which is easier accessed
# via the log files, for example using a freeware application like baretail, which
# supports highlighting, and in general helps a lot with debugging.
DEBUGTOCONSOLE = False
# ----------------------------------------------------------------------------------------

# The following URL can be used to generate the starting points for the Agents
# ----------------------------------------------------------------------------------------
url = "https://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html"
# ----------------------------------------------------------------------------------------

# Retrieve the Current Working Directory and prepare the hard coded stuff
# ----------------------------------------------------------------------------------------
cwd  = os.path.dirname(os.path.abspath(sys.argv[0]))
name = "agent-based-modelling"
logger = functions.getLogger(name, cwd, DEBUGTOCONSOLE)
# A note on Logging
""" Although I do not like this, for now, the logger instance is passed on to the agent in
    order to have continuous debug logging from all areas of the software. In the future,
    ideally, the name is passed on wherever is needed, and the logger acquired without
    passing instance references between calsses.
"""

def main():
    logger.info("Program started")
    root = tkinter.Tk()
    UI(root, logger)
    root.mainloop()


class UI:
    # Default values set as class defaults. These are used wherever a default is required.
    defNumAgents     = 10
    defNumIterations = 100
    defStepIncr      = 0
    defNeighbourhood = 20

    def __init__(self, root, lgr):
        self.keepRunning = False # Not used yet
        # Initialise the Root
        self.root = root
        self.logger = lgr
        self.root.title("Agent Based Modelling - GEOG5003M")
        self.root.resizable(False, False)
        self.root.geometry("460x650")


        # Prepare the variables
        self.outFile = os.path.join(cwd, "out.txt")
        self.storeFile = os.path.join(cwd, "store.txt")
        self.agents = []
        self.numAgents = 0
        self.numIterations = 0
        self.stepIncr = 0
        self.neighbourhood = 0
        self.environment = []
        self.xLim = 100
        self.yLim = 100

        self.url = "https://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html"
        self.urlXYData = None

        # Build the TK Interface (This required a lot of coffee)
        self.buildTkInterface()

        # Preparing the plotting stuff and displaying initially without data.
        self.fig = plt.Figure()
        self.subPlot = self.fig.add_subplot()
        self.subPlot.set_xlim(0,self.xLim)
        self.subPlot.set_ylim(0,self.yLim)
        self.subPlot.set_title ("Agents Scatter Plot", fontsize=16)
        self.subPlot.set_xlabel("X", fontsize=6)
        self.subPlot.set_ylabel("Y", fontsize=6)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()


    def buildTkInterface(self):
        bottom_frame = tkinter.Frame(self.root)
        bottom_frame.pack(side=tkinter.BOTTOM, anchor=tkinter.E, fill=tkinter.X)

        for col in range(5):
            bottom_frame.columnconfigure(col, weight=1)


        # Number of Agents
        lblNumAgents = tkinter.Label(bottom_frame, text="Agents:")
        lblNumAgents.grid(row=0, column=0, sticky=tkinter.E)
        self.entryNumAgents = tkinter.Entry(bottom_frame, width=6, bd=2)
        self.entryNumAgents.grid(row=0, column=1, sticky=tkinter.W)

        # Iterations
        lblIterations = tkinter.Label(bottom_frame, text="Iterations:", height=1)
        lblIterations.grid(row=0, column=2, sticky=tkinter.E)
        self.entryNumIterations = tkinter.Entry(bottom_frame, width=6, bd=2)
        self.entryNumIterations.grid(row=0, column=3, sticky=tkinter.W)

        # Agent Step Increment
        lblStepIncr = tkinter.Label(bottom_frame, text="Step Increment:", height=1)
        lblStepIncr.grid(row=1, column=0, sticky=tkinter.E)
        self.entryStepIncr = tkinter.Entry(bottom_frame, width=6, bd=2)
        self.entryStepIncr.grid(row=1, column=1, sticky=tkinter.W)

        # Neighbourhood
        lblNeighbourhood = tkinter.Label(bottom_frame, text="Neighbourhood", height=1)
        lblNeighbourhood.grid(row=1, column=2, sticky=tkinter.E)
        self.entryNeighbourhood = tkinter.Entry(bottom_frame, width=6, bd=2)
        self.entryNeighbourhood.grid(row=1, column=3, sticky=tkinter.W)

        # Set the label for the Environment file name display
        # --------------------------------------------------------------------------------
        self.lblEnvFile = tkinter.Label(bottom_frame, height=2, justify="left",
                                        wraplength=400, fg="blue")
        self.lblEnvFile.grid(row=2, column=0, columnspan=4, sticky=tkinter.W+tkinter.E)

        # Option to load the starting co-ordinates of the agents from URL provided by the
        # Uni
        # --------------------------------------------------------------------------------

        t = "Load the Agent Start positions from URL"
        self.v = tkinter.IntVar()
        self.chkSelectURL = tkinter.Checkbutton(bottom_frame, text=t,
                                                variable=self.v, onvalue=1, offvalue=0,
                                                command=self.chkSelectURLStateChange)
        self.chkSelectURL.grid(row=3, column=0, columnspan=4, sticky=tkinter.W)


        # Buttons
        # --------------------------------------------------------------------------------
        btnEnv = tkinter.Button(bottom_frame, width=10, command=self.loadEnvData)
        btnEnv.configure(text="Load Env.")
        btnEnv.grid(row=4, column=0, sticky=tkinter.E, padx=5, pady=5)

        # Run button is at instance level since I am changing it's state from elsewhere.
        self.btnRun = tkinter.Button(bottom_frame, text="Run", width=10, command=self.run)
        self.btnRun.grid(row=4, column=1, sticky=tkinter.W, padx=5, pady=5)

        btnStop = tkinter.Button(bottom_frame, text="Stop", width=10, command=self.stop)
        btnStop.grid(row=4, column=2, sticky=tkinter.E, padx=5, pady=5)

        btnQuit = tkinter.Button(bottom_frame, text="Quit", width=10, command=self.exitAll)
        btnQuit.grid(row=4, column=3, sticky=tkinter.W)

        # Set the label for simple notifications
        # --------------------------------------------------------------------------------
        self.lblNotify = tkinter.Label(bottom_frame, height=5, wraplength=400, fg="red",
                                       justify="left")
        self.lblNotify.grid(row=5, column=0, columnspan=4, sticky=tkinter.W+tkinter.E)
        self.lblNotify.configure(text="Simple notifications will be reported here.")
        self.setDefaultValues()

        bottom_frame.pack()


    def notify(self, m):
        """ Function to display notifications directly in the UI, bottom frame. This
            should be helpful in guiding the user.
        """
        self.lblNotify.configure(text=m,  justify="left")


    def downloadTableData(self):
        """ Function will download the data from the Leeds website. However, I decided to
            only use the x & y coordinates. The number of agents to be created will be
            equivalent to the number of coordinate pairs
        """
        self.logger.debug("Downloading table data")
        self.logger.debug(f"URL: {self.url}")
        try:
            r = requests.get(url)
            table = etree.HTML(r.text).find("body/table")
            rows = iter(table)
            headers = [col.text for col in next(rows)]
            self.urlXYData = []
            for row in rows:
                values = [col.text for col in row]
                self.urlXYData.append([int(values[0]), int(values[1])])
            self.logger.debug("Data downloaded")
        except:
            self.logger.critical("Download data failed")
            self.logger.critical(traceback.format_exc())
            self.notify("There was a problem while downloading the data")
            self.urlXYData = None


    def chkSelectURLStateChange(self):
        # This function is activated when the Checkbox to download xy data from the
        # Leeds Uni website changes the state

        # IF CHECKBOX DISABLED - Agent coordinates will be generated
        if self.v.get() == 0:
            self.notify("Coordinates will be be auto generated by the framework")
            self.urlXYData = None

        # IF CHECKBOX ENABLED - Agent Coordinates will be downloaded from the URL
        elif self.v.get() == 1:
            # Disable the Run
            self.logger.debug("Downloading the XY Data from the Leeds website")
            self.btnRun.config(state="disabled")
            self.downloadTableData()

            self.numAgents = len(self.urlXYData)
            self.entryNumAgents.delete(0, 'end')
            self.entryNumAgents.insert(0, self.numAgents)


            self.btnRun.config(state="normal")
            self.notify(f"Coordinates downloaded from {self.url}")


        self.logger.debug(self.urlXYData)

    def exitAll(self):
        """ Destroy and exit.
        """
        self.root.destroy()
        self.root.quit()


    def setDefaultValues(self):
        """ Write the default values to the instance variables. Class variables which are
            not modified programmatically are used as the source.
        """
        self.logger.debug("Setting default values to the instance variables and UI")
        # Write the defaults to the instance variables
        self.numAgents     = UI.defNumAgents
        self.numIterations = UI.defNumIterations
        self.stepIncr      = UI.defStepIncr
        self.neighbourhood = UI.defNeighbourhood
        # Write defaults also to the UI
        self.entryNumAgents.delete(0, 'end')
        self.entryNumAgents.insert(0, UI.defNumAgents)
        self.entryNumIterations.delete(0, 'end')
        self.entryNumIterations.insert(0, UI.defNumIterations)
        self.entryStepIncr.delete(0, 'end')
        self.entryStepIncr.insert(0, UI.defStepIncr)
        self.entryNeighbourhood.delete(0, 'end')
        self.entryNeighbourhood.insert(0, UI.defNeighbourhood)
        # Clear the label for the env file and disable the run... User needs to load the
        # env file again now.
        self.lblEnvFile.configure(text="Environment File Path")
        self.btnRun.config(state="disabled")
        self.chkSelectURL.configure(state="disabled")
        self.notify("Start by loading the Environment Raster data from the file.")



    def readData(self):
        """ Read the data from the TK elements, and perform very basic checks that all
            values are convertible to integers. If any value error occurs, I am assigning
        """
        try:
            self.numAgents = int(self.entryNumAgents.get())
            self.numIterations = int(self.entryNumIterations.get())
            self.stepIncr = int(self.entryStepIncr.get())
            self.neighbourhood = int(self.entryNeighbourhood.get())
            self.keepRunning = True
        except ValueError:
            self.logger.debug("ValueError exception when reading the data from the TK UI")
            self.setDefaultValues()
            self.keepRunning = False


    def loadEnvData(self):
        """ This function presents a dialog box for the user to select the environment csv
            file. It in turn uses another function to actually parse the file and return
            data.
        """
        try:
            f = tkinter.filedialog.askopenfilename(initialdir = cwd,
                                                   title = "Select a File",
                                                   filetypes = (("Text files", "*.txt*"),
                                                                ("all files", "*.*")))
            self.lblEnvFile.configure(text=f)
            if os.path.isfile(f):
                self.environment = functions.loadEnvFromCSV(f)
                self.xLim = len(self.environment[0])
                self.yLim = len(self.environment)
                self.readData()
                self.btnRun.config(state="normal")
                self.chkSelectURL.configure(state="normal")
                self.notify("You can now run the model, or select to download the coordinate data from the University site")
                self.keepRunning = True
            else:
                self.lblEnvFile.configure(text="Incorrect file, please try again")
                self.btnRun.config(state="disabled")

        except Exception as e:
            self.logger.critical("Exception occured when trying to select the env file")
            self.logger.critical(traceback.format_exc(e))

            self.lblEnvFile.configure(text="Exception occured, Please try again")


    def stop(self):
        #TODO: Implement threading and enable a stop button
        self.logger.debug("Stop")
        self.logger.debug(f"URL Data: {self.urlXYData}")

    def threading(self):
        pass
        t1=threading.Thread(target=self.run)
        t1.start()

    def createAgentsWithXY(self):
        """ Function to create the agents using the pre-downloaded x & y coordinates. This
            would eventually be part of the same logic as the createAgents function.
        """
        self.logger.debug("Creating agents with the downlaoded XY Data. Variable cleared")
        self.agents = []

        m = max(max(self.urlXYData))
        self.xLim = m
        self.yLim = m

        count = 0
        for coord in self.urlXYData:
            self.agents.append(agentframework.Agent(self.environment,
                                                    self.xLim, self.yLim, self.agents,
                                                    self.logger, coord[0], coord[1]))
            count += 1
        self.logger.debug(f"Done. {count} agents created")



    def createAgents(self, append=False):
        if append:
            self.logger.debug("Adding agents to the list")
            self.numAgents = self.stepIncr
        else:
            self.logger.debug("List of agents cleared. Creating new Agents")
            self.agents = []

        for i in range(self.numAgents):
            self.agents.append(agentframework.Agent(self.environment,
                                                    self.xLim, self.yLim, self.agents,
                                                    self.logger))
        self.logger.debug(f"{self.numAgents} agents created")
        self.logger.debug(f"Agents in list: {len(self.agents)}")


    def cleanup(self):
        """ Function to delete the store file and environment output file left over from
            the previous run. For the time being, this is not per program execution.
        """
        self.logger.info("Deleting store file and out file")
        if os.path.isfile(self.storeFile):
            try:
                os.remove(self.storeFile)
                self.logger.info(f"Store file {self.storeFile} deleted")
            except:
                self.logger.critical(f"Store file {self.storeFile} not deleted")
                self.logger.critical(traceback.format_exc())

        if os.path.isfile(self.outFile):
            try:
                os.remove(self.outFile)
                self.logger.info(f"Store file {self.outFile} deleted")
            except:
                self.logger.critical(f"Store file {self.outFile} not deleted")
                self.logger.critical(traceback.format_exc())


    def run(self):
        """ The main working function. It is important to note that whenever the run
            button is clicked, data is read again in order to be able to change parameters
            between runs.
        """
        self.cleanup()
        self.readData()

        # Logic to create agents, either by random co-ordinates, or by using the data
        # provided by the University
        # https://www.geog.leeds.ac.uk/courses/computing/practicals/python
        # /agent-framework/part9/data.html

        if self.urlXYData is not None:
            self.createAgentsWithXY()
        else:
            self.createAgents()

        # The main Iterations loop
        startTime = int(time.time())

        for x in range(self.numIterations):
            self.notify(f"Iteration {x} of {self.numIterations}")
            self.subPlot.cla()
            # x & y co-ordinate lists for plotting the scatter
            x = []
            y = []
            # The totalStore is the record of accumulated resources between the agents in
            # each iteration. This is reset at the start, and appended to a text file at
            # the end of each iteration.
            totalStore = 0

            for agent in self.agents:
                agent.move()
                agent.eat()
                agent.shareWithNeighbours(self.neighbourhood)

                x.append(agent.x)
                y.append(agent.y)

                totalStore += agent.store

            self.subPlot.set_xlim(0,self.xLim)
            self.subPlot.set_ylim(0,self.yLim)

            # Show the environment data. Note that with enough agents, this will slow
            # down
            self.subPlot.imshow(self.environment)

            self.subPlot.set_title ("Agents Scatter Plot", fontsize=16)
            self.subPlot.set_xlabel("X", fontsize=6)
            self.subPlot.set_ylabel("Y", fontsize=6)
            self.subPlot.scatter(x, y, marker=".", color='red')
            self.canvas.draw()

            # Append the store data to the output store file
            with open(self.storeFile, "at") as of:
                of.write(f"{totalStore}\n")

            # If the Step Increment is greater than 0, between each run, agents are added
            # to the agents list. The upper limit of 10 is there due to performance issues
            if 0 < self.stepIncr <= 10:
                self.createAgents(append=True)



        self.logger.info("Writing the updated environment data to the output file.")
        functions.saveEnvToCSV(self.environment, self.outFile)

        endTime = int(time.time())

        txt = (f"Finished :) It took {endTime-startTime} seconds for {len(self.agents)} "
               f"agents to complete a run of {self.numIterations} iterations!")

        self.notify(txt)

        self.logger.info(txt)
































if __name__ == "__main__":
    main()
