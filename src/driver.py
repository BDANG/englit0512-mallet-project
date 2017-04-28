#This python program is designed to showcase the functionality of my work

import sys
from TopicSimilarity import TopicSimilarity
from TopicDistribution import TopicDistribution
from TopicProximity import TopicProximity

MALLET_MODEL = None #global is assigned to the mallet model from the command line argument

#This method simply iterates the mallet file line-by-line
#and returns a list of the filenames found in the mallet file
def get_filenames_in_mallet_output(malletfile):
    filenameList = []
    for line in malletfile:
        if line.startswith("#"): #skip the lines starting with #
            continue
        filename = line.split(" ")[1].split("/")[-1] #parse the filename (without the path)
        if filename not in filenameList: #add the filename to the list if it is not in the list already
            filenameList.append(filename)
    return filenameList

def main(args):
    global MALLET_MODEL

    #validate the command line input
    if (len(args) != 2):
        print args[0]+" requires the document generated from using the option \"--output-state <name.gz>\" when training topics with mallet"
        print "\tYou can retrieve the file from \">bin/mallet train-topics --input <input.mallet> --num-topics [num] --output-state <name.gz>\""
        print "\tthen tar -xzvf <name.gz>"
        print "\nRun as "+args[0]+" <mallet_output>"
        sys.exit(-1)
    else:
        MALLET_MODEL = args[1] #assign the global

    #confirm the input argument was a valid file
    try:
        malletfile = open(MALLET_MODEL, "r")
    except:
        print "\nIt appears "+MALLET_MODEL+" was not a valid file."
        print "You can run as python "+args[0]+" for help"
        sys.exit(-1)

    #get the possible file names to show to the user later
    possibleFileNames = get_filenames_in_mallet_output(malletfile)
    malletfile.close()


    #driver menu
    while True:
        print "\nHere are your options:"
        print "\t1. Topic Distribution Over the Course of a Text"
        print "\t2. Topic Similarity"
        print "\t3. Topic Proximity for a Text"
        print "\tq. To quit"
        choice = raw_input("Choice: ")
        if (choice == "1"): #topic distribution function
            #show the filenames found in the mallet model
            print ("\nHere are the possible files for distribution analysis:")
            for fname in possibleFileNames:
                print "\t"+fname
            fileToAnalyze = raw_input("What file (must be in "+MALLET_MODEL+") do you want to see the distribution? ")

            #create instance of the class using the mallet model and the filename to analyze
            TopicDistribution(MALLET_MODEL, fileToAnalyze).create()
        elif (choice == "2"): #topic similarity
            #create instance of the class using the mallet model and analyze
            TopicSimilarity(MALLET_MODEL).create()
        elif (choice == "3"): #topic proximity
            #show the filenames found in the mallet model
            print ("\nHere are the possible files for distribution analysis:")
            for fname in possibleFileNames:
                print "\t"+fname
            fileToAnalyze = raw_input("What file (must be in "+MALLET_MODEL+") do you want to see the Topic Proximity? ")

            #create instance of the class using the mallet model and the filename to analyze
            TopicProximity(MALLET_MODEL, fileToAnalyze).create()
        elif (choice == "q"): #exit
            break
        else:
            print "\n\nThe choice was not recognized. Just enter the number corresponding to the option."
            try:
                raw_input("Enter anything to return to the menu.")
            except:
                continue




main(sys.argv)
