#This python program is designed to showcase the functionality of my work
import sys
from TopicSimilarity import TopicSimilarity
from TopicDistribution import TopicDistribution

MALLET_MODEL = None

def get_filenames_in_mallet_output(malletfile):
    filenameList = []
    for line in malletfile:
        if line.startswith("#"): #skip the lines starting with #
            continue
        filename = line.split(" ")[1].split("/")[-1]
        if filename not in filenameList:
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

    #driver menu
    while True:
        print "\nHere are your options:"
        print "\t1. Topic Distribution Over the Course of a Text"
        print "\t2. Topic Similarity"
        print "\tq. To quit"
        choice = raw_input("Choice: ")
        if (choice == "1"): #topic distribution function

            #get the possible file names to show to the user
            possibleFileNames = get_filenames_in_mallet_output(malletfile)
            print ("\nHere are the possible files for distribution analysis:")
            for fname in possibleFileNames:
                print "\t"+fname
            fileToAnalyze = raw_input("What file (must be in "+MALLET_MODEL+") do you want to see the distribution? ")

            #create instance of the class using the mallet model and the file to analyze
            TopicDistribution(MALLET_MODEL, fileToAnalyze).create()
        elif (choice == "2"):
            #create instance of the class using the mallet model and analyze
            TopicSimilarity(MALLET_MODEL).create()
        elif (choice == "q"): #exit
            break
        else:
            print "\n\nThe choice was not recognized. Just enter the number corresponding to the option."
            try:
                raw_input("Enter anything to return to the menu.")
            except:
                continue

    malletfile.close()



main(sys.argv)
