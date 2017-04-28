# Brian Dang's ENGLIT 0512 Final Project
This is a repo of my work regarding visualizations of MALLET topic models

## Notes
 - Currently, it is expected of the user to know how to use the MALLET command line tool
    - See the Preparation section below for a quick demo
 - Future work implementing my work should already have a means of automating the MALLET command line as it is trivial operation
 - Although it is written in Python, you could use Java's ```Runtime.getRuntime().exec("python ...")``` to call the python programs

## Functionality 
 1. Topic Distribution over the Course of a Given Text
    - Topic Distribution visualizes how topics appear in portions of the a text.
    - __Usefulness__: The functionality enables analyzers to understand the how portions of a text change in relation to the topics. The information may lead to subsetting portions of a text that have strong occurrences of a topic in order to strengthen the topic model.
 2. Topic Similarity
    - Topic Similarity visualizes how unique words in a topic appear in a different topic
    - Similarity is simply defined as the # of common words between two topics divided by the average size of the two topics
    - Currently, the functionality only relies on unique words in a topic. One could theoretically modify the code to somehow account for the number of occurrences of a word in a topic and calculate topic similarity based on the top N words of a topic, or somehow use the number of occurences to weight the similarity, etc.
    - __Usefulness__: MALLET is pretty good at formulating distinct topics, however it is not a perfect system. Topic Similarity allows analyzers to visualize the distinctness of topics. This information may allow them to tweak their training parameters to produce more distinct topics.


## Preparation
Stated previously, the MALLET model needs to be populated beforehand.
Here is a sample preparation and relies on most of MALLET's default values:

Inside the MALLET directory:
```
bin/mallet import-dir --input <path to directory of .txt> --keep-sequence --remove-stopwords --output demo.mallet

bin/mallet train-topics --input demo.mallet --num-topics 25 --output-state demo_output.gz

gunzip -k demo_output.gz
```
After extracting with gunzip, you'll have a demo_output file. This is the file you want to pass to the program:

```python driver.py <path to demo_output>```

### Understanding the Graphs
 - See the Graph_Examples.pdf

### Requirements
 - Python 2.7
 - Python Plot.ly API: https://plot.ly/python/
 - MALLET: http://mallet.cs.umass.edu/

#### Additional Credits
 - MALLET: http://mallet.cs.umass.edu/
 - Plot.ly API: https://plot.ly/python/
