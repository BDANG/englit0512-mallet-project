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
    - Usefulness: MALLET is pretty good at formulating distinct topics, however it is not a perfect system. Topic Similarity allows analyzers to visualize the distinctness of topics. This information may allow them to tweak their training parameters to produce more distinct topics.
    - Currently, the functionality only relies on unique words in a topic. One could theoretically modify the code to somehow account for the number of occurrences of a word in a topic and calculate topic similarity based on the top N words of a topic, etc.

## Preparation
Stated previously, the MALLET output needs to be populated beforehand.
Here is a sample preparation:

## Requirements
 - Python 2.7
 - Python Plot.ly API
 - MALLET

#### Additional Credits
 - MALLET: http://mallet.cs.umass.edu/
 - Plot.ly API: https://plot.ly/python/
