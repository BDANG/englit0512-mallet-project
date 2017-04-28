import plotly
import plotly.graph_objs as graphobj

NUMBER_OF_BINS = 25 #number of bins for the histogram x-axis. You can modify this!

class TopicDistribution:
    malletModel = None #variable stores the filename+path of the mallet output
    filename = None
    def __init__(self, malletModel, filename):
        self.malletModel = malletModel
        self.filename = filename
    def create(self):
        print "\nCreating a Topic Distribution for "+self.filename

        uniqueTopicNumbers = [] #list of unique topic numbers
        topicOrder = [] #stores the sequence of topics based on the sequence of the words like 3, 4, 2, 3, 6, 2, etc

        malletFile = open(self.malletModel, "r")
        for line in malletFile:
            #split the line in mallet file by space
            splits = line.split(" ")
            filename = splits[1].split("/")[-1] #get the filename, which is the last element of the path
            if (filename != self.filename): #don't care about data for the other filenames
                continue;

            topicNum = int(splits[5])
            topicOrder.append(topicNum) #add the topic number to the end of the list
            if topicNum not in uniqueTopicNumbers:
                uniqueTopicNumbers.append(topicNum)

        uniqueTopicNumbers = sorted(uniqueTopicNumbers)

        distribution = {} #maps topic number to a list of occurrences.
                          #example: distribution[3] = [20, 60, 10] means topic number 3 occurs 20x times in the first third, 60x times in the second third, 10x in the last third
        currentDistribution = {} #reset with each bin. but for each bin:
                                 #maps topic number to the number of occurences
                                 #example: currentDistribution[3] = 60 means for this bin, topic number 3 occurs 60x times

        for t in uniqueTopicNumbers:
            distribution[t] = [] #initialize the distribution key to an empty list
            currentDistribution[t] = 0 #initialize the key with 0

        #determine the number of elements in each bin by dividing the number of words into the NUMBER_OF_BINS
        elementsPerBin = len(topicOrder) / NUMBER_OF_BINS

        topicCounter = 0
        for topic in topicOrder:
            currentDistribution[topic] += 1

            topicCounter += 1
            if topicCounter == elementsPerBin:
                topicCounter = 0
                for t in uniqueTopicNumbers:
                    distribution[t].append(currentDistribution[t])
                    currentDistribution[t] = 0 #reset

        for x in distribution.keys():
            print str(x)+": "+str(distribution[x])

        print len(topicOrder)
        print len(distribution[8])
