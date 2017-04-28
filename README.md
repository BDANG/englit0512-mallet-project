# Brian Dang's ENGLIT 0512 Final Project
This is a repo of my work regarding visualizations of MALLET output

## Notes
 - Currently, it is expected of the user to know how to use the MALLET command line tool
 - Future work implementing my work should already have a means of automating the MALLET command line as it is trivial operation
 - Although it is written in Python, you could use Java's Runtime.getRuntime().exec("python ...") to call the python programs

## Functionality
 1. Topic Distribution over the Course of a Given Text
 2. Topic Similarity
    - Topic Similarity visualizes how unique words in a topic appear in a different topic
    - Similarity is simply defined as the # of common words between two topics divided by the average size of the two topics
## Requirements
 - Python 2.7
 - Python Plot.ly API
 - MALLET

#### Additional Credits
 - MALLET: http://mallet.cs.umass.edu/
 - Plot.ly API: http://mallet.cs.umass.edu/
