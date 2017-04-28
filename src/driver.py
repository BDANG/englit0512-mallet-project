#This python program is designed to showcase the functionality of my work
import sys
from TopicSimilarity import TopicSimilarity

MALLET_MODEL = None
def main(args):
    global MALLET_MODEL
    if (len(args) != 2):
        print args[0]+" requires the document generated from using the option \"--output-state <name.gz>\" when training topics with mallet"
        print "\tYou can retrieve the file from \">bin/mallet train-topics --input <input.mallet> --num-topics [num] --output-state <name.gz>\""
        print "\tthen tar -xzvf <name.gz>"
        print "\nRun as "+args[0]+" <mallet_output>"
        sys.exit(-1)
    else:
        MALLET_MODEL = args[1]
    while True:
        print "\nHere are your options:"
        print "\t1. Topic Distribution Over the Course of a Text"
        print "\t2. Topic Similarity"
        print "\tq. To quit"
        choice = str(input("Choice: "))
        if (choice == "1"):
            print "Topic Distribution"
        elif (choice == "2"):
            print "Topic Similarity"
            TopicSimilarity(MALLET_MODEL).create()
        else:
            print "\n\nThe choice was not recognized. Just enter the number corresponding to the option."
            try:
                input("Enter anything to return to the menu.")
            except:
                continue


main(sys.argv)
