import sys
import argparse



def parseArguments():
    parser = argparse.ArgumentParser(description="Agent Simulator. Random agents \
                                                  interacting with the environment and \
                                                  each other.")

    parser.add_argument("-a", dest="numAgents", default=10,
                        help='The number of Agents to spawn. Default is 10.')

    parser.add_argument("-i", dest="numIterations", default=100,
                        help="Iterations to run through. Default is 100")

    parser.add_argument("-n", dest="neighbourhood", default=20,
                        help="Neighbourhood distance. Default is 20")

    args = parser.parse_args()

    try:
        numAgents = int(args.numAgents)
        numIterations = int(args.numIterations)
        neighbourhood = int(args.neighbourhood)
    except ValueError:
        print("Values all need to be integers")
        print("Proceeding with the default variables")

        defaults = {}
        for key in vars(args):
            defaults[key] = parser.get_default(key)

        numAgents = defaults["numAgents"]
        numIterations = defaults["numIterations"]
        neighbourhood = defaults["neighbourhood"]
    finally:
        print("numAgents ",numAgents)
        print("numIterations ",numIterations)
        print("neighbourhood ",neighbourhood)


parseArguments()

#if __name__ == "__main__":
    #main()
