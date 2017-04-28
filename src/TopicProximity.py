#This class is used to create a heatmap of topic proximity

import plotly
import plotly.graph_objs as graphobj

#custom color scale for the plot.ly heatmap!
customColorScale = [
    [0, 'rgb(0, 0, 255)'],
    #[0.125, 'rgb(0, 128, 255)'],
    [0.25, 'rgb(0, 255, 0)'],
    #[0.375, 'rgb(0, 255, 128)'],
    [0.50, 'rgb(255, 255, 0)'],
    #[0.625, 'rgb(128, 255, 0)'],
    [0.75, 'rgb(255, 128, 0)'],
    #[0.875, 'rgb(255, 128, 0)'],
    [1.0, 'rgb(255, 0, 0)']
]

#specifies how many words to consider for proximity
#i.e. if it is 100, every 100 words in the file are considered be a chunk
NUMBER_OF_WORDS_PER_CHUNK = 100 #You can change this!

class TopicProximity:
    malletModel = None #variable stores the filename+path of the mallet output
    filename = None #filename to be analyzed
    def __init__(self, malletModel, filename):
        self.malletModel = malletModel
        self.filename = filename

    #This method handles the update of the heatdata
    #
    #heatdata: the 2D array used as the data for Plot.ly heatmap
    #topicCounts: a dictionary that maps topic number -> counts
    #topics: an ordered list the topic numbers
    #
    #for each topic pair combination, sum the counts of the topics and increase the 2D array
    #afterwords, the heatdata sums will be averaged by dividing each sum by the number of chunks analyzed
    def update_proximity(self, heatdata, topicCounts, topics):
        for topic1 in topics: #for each topic pair combination
            for topic2 in topics:
                if topic1 == topic2: #skip the topic pair combinations that are the same topics
                    continue
                #add the sum of the counts to the 2D array
                heatdata[topic1][topic2] += (topicCounts[topic1] + topicCounts[topic2])

    #This method will parse the mallet model to create a heatmap of topic proximity for the filename
    #topic proximity represents how the topics are found together in chunks the size of NUMBER_OF_WORDS_PER_CHUNK
    #
    #defining topic proximity:
    #   a value for a pair of topics represents how many of the words in NUMBER_OF_WORDS_PER_CHUNK originated from the two topics
    #   Example: (5, 2): 70 and NUMBER_OF_WORDS_PER_CHUNK = 100
    #       this means topic number 5 and topic number 2 appear, on average, 70x times every 100 words
    #
    #calculating topic proximity:
    #   every NUMBER_OF_WORDS_PER_CHUNK, a count of each topic number is maintained
    #   for every pair of topic number combinations, the counts are summed together
    #   at the end, each sum is divided by the number of chunks analyzed
    def create(self):
        print "\nCreating a Heatmap of Topic Proximity for: "+self.malletModel

        uniqueTopicNumbers = [] #list of unique topic numbers
        topicOrder = [] #stores the sequence of topics based on the sequence of the words. example: 3, 4, 2, 3, 6, 2, etc


        #open the mallet output and parse it line-by-line
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

        currentTopicCount = {} #for each chunk, map the topic number to the count the number of topics
                               #example: for a given chunk, if currentTopicCount[4] = 10, topic 4 was found 10x times

        #initialize the dictionary that were just declared
        for t in uniqueTopicNumbers:
            currentTopicCount[t] = 0

        #init 2d array with 0 for the heatmap
        heatdata=[[0 for i in range(len(uniqueTopicNumbers))] for i2 in range(len(uniqueTopicNumbers))]

        #iterate the topic sequence
        counter = 0 #counts how many topics iterated
        chunkCounter = 0 #counts how many chunks were analyzed
        for topic in topicOrder:
            currentTopicCount[topic] += 1 #count the topic number
            counter+=1 #count the topics iterated
            if counter == NUMBER_OF_WORDS_PER_CHUNK: #means the loop iterated a chunk of topics
                counter = 0 #reset the counter
                chunkCounter+=1 #count the chunk as being analyzed

                #update the heatmap data
                self.update_proximity(heatdata, currentTopicCount, uniqueTopicNumbers)

                #reset for the next chunk
                for t in uniqueTopicNumbers:
                    currentTopicCount[t] = 0 #reset the topic number counter

        #for each value in heatdata, we average it by dividing each value by the number of chunks analyzed
        for i1 in range(len(uniqueTopicNumbers)):
            for i2 in range(len(uniqueTopicNumbers)):
                heatdata[i1][i2] = float(heatdata[i1][i2])/chunkCounter

        #make the heatmap object
        trace = graphobj.Heatmap(
            z = heatdata,
            zmin = 0.0,
            zmax = NUMBER_OF_WORDS_PER_CHUNK,
            x=uniqueTopicNumbers,
            y=uniqueTopicNumbers,
            colorscale = customColorScale
        )

        #graph the heatmap
        plotly.offline.plot({
            "data": [trace], #graph the trace that was populated above

            #format stuff:
            "layout": dict(

                #graph title
                title = "Topic Proximity for "+self.filename,

                #xaxis label
                xaxis = dict(
                    title = "Topic Number",
                    showticklabels=True
                ),

                #yaxis label
                yaxis = dict(
                    title = "Topic Number",
                    showticklabels=True
                )
            )
        }, filename="../plotly_output/heatmap_topic_proximity")
