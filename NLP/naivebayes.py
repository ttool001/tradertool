#import nltk library
import nltk as nltk
from nltk.metrics import precision, recall, f_measure
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
#import csv library to read csv files
import csv
from twittertest import getTweets

#initialize arrays
pos_tweets = []
neg_tweets = []
pos_test_tweets = []
neg_test_tweets = []
test_tweets = []
tweets = []


#read csv training file with tweets
f = open('/Users/derekyu/projects/NLP Project/NLP-Project/FinalProject/training.manual.2009.06.14.csv', 'r')
csv_f = csv.reader(f)


#iterate through rows in fle
#first element of row (csv_row[0]) is the word positive or negative, which is the sentiment
#if row[0] is positive create a tuple of 2 elements that stores the tweet in the row and the string 'positive', then append that to a list of positive tweets
#the tweet in the row is the 2nd element
#if csv_row[0] is negative, create a tuple of 2 elements that stores the tweet in the row and the string 'negative', then append that to a list negative tweets
for csv_row in csv_f:
    if(csv_row[0] == '4'):
        pos = (csv_row[5], 'positive')
        pos_tweets.append(pos)
    else:
        if(csv_row[0] == '0'):
            neg = (csv_row[5], 'negative')
            neg_tweets.append(neg)


#convert tweets to lowercase and remove any word less than 3 characters
for (words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

#extract words from tweets and return in the list all_words
def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

#extract the list of distinct words and return in the list word_features
def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features


#call the functions get_word_features and get_word_in_tweets to get the list of word features (list of every distinct word ordered by frequency of appearance)
word_features = get_word_features(get_words_in_tweets(tweets))

#function to extract relevant features (words in the tweet inputted) and return a dictionary that is created using the word_features list and the words in the input
#the dictionary indicates whether the words in the input are contained in the word features list
def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

def classifyTweets(classifier):
    positive_tweets = []
    negative_tweets = []
    new_tweets = getTweets()
    for tweet in new_tweets:
        #print tweet
        process_tweet = extract_features(tweet)
        #print classifier.classify(process_tweet)


#use the nltk classify and apply_features methods to apply the features to the features in the tweets list defined above and store in training_set
#training set is a list of tuples with the feature dictionary defined above and the sentiment for each tweet
training_set = nltk.classify.apply_features(extract_features, tweets)

#use the nltk Naive Bayes Classifier method to train the training set
classifier = nltk.NaiveBayesClassifier.train(training_set)

classifyTweets(classifier)

#read the test data csv file
f1 = open('/Users/derekyu/projects/NLP Project/NLP-Project/FinalProject/berniesanderstestfile.csv','r')
csv_f1 = csv.reader(f1)

for csv_row in csv_f1:
    if(csv_row[0] == 'positive'):
        pos = (csv_row[1], 'positive')
        pos_test_tweets.append(pos)
    else:
        if(csv_row[0] == 'negative'):
            neg = (csv_row[1], 'negative')
            neg_test_tweets.append(neg)

for (words, sentiment) in pos_test_tweets + neg_test_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    test_tweets.append((words_filtered, sentiment))

test_set = nltk.classify.apply_features(extract_features, test_tweets)
print(test_set)
f1 = open('/Users/derekyu/projects/NLP Project/NLP-Project/FinalProject/berniesanderstestfile.csv','r')
csv_f1 = csv.reader(f1)
#classify and print out as either positive or negative
for row in csv_f1:
    print(classifier.classify(extract_features(row[1].split())))

def classifier_stats(classifier,test_set):
    import collections
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    for i, (sample, label) in enumerate(test_set):
        refsets[label].add(i)
        observed = classifier.classify(sample)
        testsets[observed].add(i)

    print ('pos precision:', precision(refsets['positive'], testsets['positive']))
    print ('pos recall:', recall(refsets['positive'], testsets['positive']))
    print ('pos F-measure:', f_measure(refsets['positive'], testsets['positive']))
    print ('neg precision:', precision(refsets['negative'], testsets['negative']))
    print ('neg recall:', recall(refsets['negative'], testsets['negative']))
    print ('neg F-measure:', f_measure(refsets['negative'], testsets['negative']))

classifier_stats(classifier, test_set)