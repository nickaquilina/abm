# Agent Based Modelling


## GEOG5003M - Programming for Geographical Information Analysis

Nicholas Aquilina 2021


Agent based modelling scripts for an assignment at the University of Leeds.

All code is in Python, and isthe model is used to simulate movement and manipulation of the environment. An Agent-based model is highly iterative, in that the effect can be seen after a number (usually large) of iterations.

The Agents move around randomly, one step at a time, until either the iteration limit or an other condition have been reached. In my case, this version is based on the number of iterations only.

## Source Files Contained

* **model_cli.py**
	* Model to be executed via command line. No UI is available, except for the plotting window. Being purely command line, this script uses the argparse builtin library in order to parse user input. Note that this may not be as up-to-date as the proper GUI Application, since this was there mainly for the practicals. The GUI Application is the main Application

* **model_gui.py**
	* Model version containing a TK UI. All options are configurable via the UI, except for the verbose. That is configurable directly from the script in the form of a variable. I wanted to move that as an argument when starting the application, however, did not, due to time constraints.

* **agentframework.py**
	* The source file contains the Agent Class for the model. This can be used by both model versions.

* **in.txt**
	* A CSV file containing the 2D Raster resources data

* **out.txt**
	* An updated CSV file that is the result of resource gathering and depositing during the function of the model. Note that this file is not available for download. It is automatically saved after a run.

* **functions.py**
	* Other functions, also critical for the functioning of the ABM. Some functions which are still in this file should have been moved to the model source file, however I did not manage that due to time constaints.


## Starting the program

**>python model_gui.py**


## Logging

I used the python logging module in order to provide details logs of what the script is doing. This was especially useful during development. For advanced logging, the variable "DEBUG = False" in the main model_cli.py file needs to be set to True. This essentially enables the logging of DEBUG level to file as well. Only informaiton messages are displayed via STDOUT, so that the user is not overloaded.

