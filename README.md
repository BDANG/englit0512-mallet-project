# Brian Dang's ENGLIT 0512 Final Project
This is a repo of my work regarding visualizations of MALLET topic models.

## Notes
 - Currently, it is expected of the user to know how to use the MALLET command line tool.
    - See the Preparation section below for a quick demo.
 - Future work implementing my work should already have a means of automating the MALLET command line as it is trivial operation.
 - Although it is written in Python, you could use Java's ```Runtime.getRuntime().exec("python ...")``` to call the python programs.

## Functionality
 1. Topic Distribution over the Course of a Given Text
    - Topic Distribution visualizes how topics appear in portions of the a text.
    - The number of the bins can be modified by changing the value of ```NUMBER_OF_BINS``` in ```TopicDistribution.py```
        - i.e. changing to 50 would mean the text is broken into 50 bins
    - The filename that is passed to the ```TopicDistribution``` class is verified by the driver. Usage of ```TopicDistribution``` assumes that the filename argument passed to it appears in the mallet model file.
    - __Usefulness__: The functionality enables analyzers to understand the how portions of a text change in relation to the topics. The information may lead to subsetting portions of a text that have strong occurrences of a topic in order to strengthen the topic model.
 2. Topic Similarity
    - Topic Similarity visualizes how unique words in a topic appear in a different topic.
    - Similarity is simply defined as the # of common words between two topics divided by the average size of the two topics.
    - Currently, the functionality only relies on unique words in a topic. One could theoretically modify the code to somehow account for the number of occurrences of a word in a topic and calculate topic similarity based on the top N words of a topic, or somehow use the number of occurences to weight the similarity, etc.
    - __Usefulness__: MALLET is pretty good at formulating distinct topics, however it is not a perfect system. Topic Similarity allows analyzers to visualize the distinctness of topics. This information may allow them to tweak their training parameters to produce more distinct topics.
 3. Topic Proximity for a Text
    - Topic Proximity visualizes how different topics occur within the same chunk of text from an average perspective.
    - The size of each chunk can be modified by changing ```NUMBER_OF_WORDS_PER_CHUNK``` in ```TopicProximity.py```
        - i.e. changing to 200 would mean chunks are analyzed every 200 words.
    - The filename that is passed to the ```TopicProximity``` class is verified by the driver. Usage of ```TopicProximity``` assumes that the filename argument passed to it appears in the mallet model file.
    - __Usefulness__: The heatmap identifies which topics appear proximate to one another from an average perspective. Topics that appear often with another topic reveal a sort of synergy with each other. If an analyzer is interested in a specific topic, the ```TopicProximity``` functionality will allow the analyzer to find another topic that occurs frequently with their interested topic.


## Preparation
Stated previously, the MALLET model needs to be populated beforehand.
Here is a sample preparation and relies on most of MALLET's default values:

Inside the MALLET directory:
```
bin/mallet import-dir --input <path to directory of .txt> --keep-sequence --remove-stopwords --output demo.mallet

bin/mallet train-topics --input demo.mallet --num-topics 25 --output-state demo_output.gz

gunzip -k demo_output.gz
```
After extracting with gunzip, you'll have a ```demo_output``` file. This is the file you want to pass to the program:

```python driver.py <path to demo_output>```

### Understanding the Graphs
All the sample graphics were created using default MALLET options on corpus found in ```books/```. Modelling with 10 topics and 20 topics were examined.
 - Topic Distribution
    - ![](sample_output/topic_distribution_peter_10_topics.png?raw=true "Topic Distribution of Peter Pan with 10 Topics")

### Requirements
 - Python 2.7
 - Python Plot.ly API: https://plot.ly/python/
 - MALLET: http://mallet.cs.umass.edu/

#### Additional Credits
 - MALLET: http://mallet.cs.umass.edu/
 - Plot.ly API: https://plot.ly/python/
