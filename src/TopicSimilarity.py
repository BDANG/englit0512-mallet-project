#This class is used to create a heatmap of topic similarity

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

class TopicSimilarity:
    malletModel = None #variable stores the filename+path of the mallet output
    def __init__(self, malletModel):
        self.malletModel = malletModel

    #Similarity is defined as the # of common words divided by the average size of the wordsets
    #example:
    #   wordset1 = {brian, dang, is, cool}
    #   wordset2 = {my, name, is, brian, dang}
    #
    #   common words = 3 from (brian, dang, is)
    #   average size = 4.5 from (4+5)/2
    #   similarity = .666
    #
    #   wordSet1: a set of unique words found in a topic
    #   wordSet2: a set of unique words foun in a topic
    def calc_similarity(self, wordSet1, wordSet2):
        intersectionLength = len(wordSet1.intersection(wordSet2)) # number of common words
        avgLength = float(len(wordSet1)+len(wordSet2))/2 #average length
        return float(intersectionLength/avgLength) #similarity = common words / average length

    #This method will parse the mallet output to create a heatmap of topic similarity
    #topic similarity essentially means "the percentage of unique words in a topic that are found in another topic"
    #
    #first: parse the mallet output into a dictionary
    #   dictionary maps topic number -> unique words in the topic
    #second: iterate the topic numbers against each other, calculate similarity
    #last: graph the similarity with a Plot.ly Heatmap
    def create(self):
        print "\nCreating a Heatmap of Topic Similarity for: "+self.malletModel
        topicWordsDict = {} #maps topic number to the unique words in the topic


        #open the mallet output and parse it line-by-line
        malletFile = open(self.malletModel, "r")
        for line in malletFile:
            if line.startswith("#"): #required to skip the first few lines of the mallet file
                continue

            #split the line in mallet file by space
            splits = line.split(" ")
            word = splits[4] #word is the 5th element
            topicNum = int(splits[5]) #topic number for the word is the 6th element

            #add the topic number and word to the dictionary if it doesnt exist
            if topicNum not in topicWordsDict:
                topicWordsDict[topicNum] = set()
                topicWordsDict[topicNum].add(word)
            else: #otherwise, just add the word to the topic num
                topicWordsDict[topicNum].add(word)


        malletFile.close()

        #init 2d array with 0 for the heatmap
        heatdata=[[0 for i in range(len(topicWordsDict.keys()))] for i in range(len(topicWordsDict.keys()))]

        #doubly iterate the topic numbers to compare topic number against topic number
        topicNumbers = sorted(topicWordsDict.keys()) #order list of topic numbers to iterate
        for topic1 in topicNumbers:
            for topic2 in topicNumbers:
                if (topic1 == topic2): #if the topic numbers are the same, we expect the similarity to be 100% so just short circuit the case
                    heatdata[topic1][topic2] = 100.0
                    continue
                #otherwise, the topic numbers are different. compute similarity
                heatdata[topic1][topic2] = (self.calc_similarity(topicWordsDict[topic1], topicWordsDict[topic2]))*100.0


        #make the heatmap object
        trace = graphobj.Heatmap(
            z = heatdata,
            zmin = 0.0,
            zmax = 100.0,
            x=topicNumbers,
            y=topicNumbers,
            colorscale = customColorScale
        )

        #graph the heatmap
        plotly.offline.plot({
            "data": [trace], #graph the trace that was populated above

            #format stuff:
            "layout": dict(

                #graph title
                title = "Topic Similarity",

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
        }, filename="../plotly_output/heatmap_topic_similarity")
