import plotly
import plotly.graph_objs as graphobj

NUMBER_OF_BINS = 25 #number of bins for the histogram x-axis. You can modify this!

class TopicDistribution:
    malletModel = None #variable stores the filename+path of the mallet output
    filename = None
    def __init__(self, malletModel, filename):
        self.malletModel = malletModel
        self.filename = filename

    #This method handles the parsing of the mallet output file and generating a topic distribution for a filename in the mallet output
    def create(self):
        print "\nCreating a Topic Distribution for "+self.filename

        uniqueTopicNumbers = [] #list of unique topic numbers
        topicOrder = [] #stores the sequence of topics based on the sequence of the words. example: 3, 4, 2, 3, 6, 2, etc

        malletFile = open(self.malletModel, "r")
        for line in malletFile:
            if line.startswith("#"): #skip the lines starting with #
                continue

            #split the line in mallet file by space
            splits = line.split(" ")
            topicNum = int(splits[5])
            filename = splits[1].split("/")[-1] #get the filename, which is the last element of the path

            if topicNum not in uniqueTopicNumbers: #don't forget to maintain the list of unique topic numbers
                uniqueTopicNumbers.append(topicNum)

            if (filename != self.filename): #don't care about data for the other filenames
                continue
            topicOrder.append(topicNum) #add the topic number to the end of the list


        malletFile.close()

        uniqueTopicNumbers = sorted(uniqueTopicNumbers) #sort the topic numbers

        totalTopicOccurences = {} #maps a topic number to the total number of occurences
                                  #example: totalTopicOccurences[4] = 100 means that topic number 4 occurs 100 times in the text

        distribution = {} #maps topic number to a list of occurrences.
                          #example: distribution[3] = [20, 60, 10] means topic number 3 occurs 20x times in the first third, 60x times in the second third, 10x in the last third

        percentDistribution = {} #maps topic number to a list of percentages
                                 #example: percentDistribution[4] = [.22, .66, .11] means the 22% of topic 4 appears in the first third
                                 #the dictionary is populated, but currently unused. May be worthwhile for future work

        currentDistribution = {} #reset with each bin. but for each bin:
                                 #maps topic number to the number of occurences
                                 #example: currentDistribution[3] = 60 means for this bin, topic number 3 occurs 60x times

        #initialize all the dictionaries that were just declared
        for t in uniqueTopicNumbers:
            distribution[t] = []
            currentDistribution[t] = 0
            totalTopicOccurences[t] = 0
            percentDistribution[t] = []

        #determine the number of elements in each bin by dividing the number of words into the NUMBER_OF_BINS
        elementsPerBin = len(topicOrder) / NUMBER_OF_BINS

        topicCounter = 0 #a counter to determine when the next bin is being analyzed
        for topic in topicOrder:
            totalTopicOccurences[topic] += 1 #keep track of the total occurences
            currentDistribution[topic] += 1 #keep track of the occurences for this bin

            topicCounter += 1
            if topicCounter == elementsPerBin: #have filled a bin, so flush it to the distribution dictionary and reset the currentDistribution
                topicCounter = 0
                for t in uniqueTopicNumbers: #need to repeat for all the topic numbers
                    distribution[t].append(currentDistribution[t]) #flush the bin to the distribution
                    currentDistribution[t] = 0 #reset


        #create a trace for each topic number
        tracelist = []
        for topicNum in uniqueTopicNumbers: #iterate the topic numbers
            distributionList = distribution[topicNum] #the y values of the graph

            #add a trace for each topic number to a list
            tracelist.append(graphobj.Scatter(
                    x = [i+1 for i in range(NUMBER_OF_BINS+1)], #x values are the bins
                    y = distributionList,
                    name = "Topic Number "+str(topicNum) #label is the topic number
                )
            )

            #this is the unused percent distribution
            totalTopicCount = totalTopicOccurences[topicNum]
            for d in distributionList:
                #percentage distribution is the # of occurences (d) divided by the total # of occurences
                if totalTopicCount != 0:
                    percentDistribution[topicNum].append(float(d)/float(totalTopicCount))
                else:
                    percentDistribution[topicNum].append(0)


        #graph the data
        plotly.offline.plot({
            "data": tracelist, #trace list populated directly above

            #format stuff:
            "layout": dict(
                #graph title:
                title = "Topic Distribution for "+self.filename,

                #xaxis label
                xaxis = dict(
                    title = "Portion of the Text",
                    showticklabels=True
                ),

                #yaxis label
                yaxis = dict(
                    title = "Occurences of a Topic",
                    showticklabels=True
                )
            )
        }, filename="../plotly_output/linegraph_topic_distribution")
