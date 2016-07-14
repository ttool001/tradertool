import nltk
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from classifier import TweetClassifier


bayesDoc2 = open('naivebayes2.pickle', 'rb')
bayesClassifier2 = pickle.load(bayesDoc2)
bayesDoc2.close()
bayesDoc = open('Bernoulli_classifier.pickle', 'rb')
bayesClassifier = pickle.load(bayesDoc)
bayesDoc.close()

mnbDoc = open('MNB_classifier.pickle', 'rb')
mnbClassifier = pickle.load(mnbDoc)
mnbDoc.close()

logisticDoc = open('LogisticRegression_classifier.pickle', 'rb')
logisticClassifier = pickle.load(logisticDoc)
logisticDoc.close()

linearDoc = open('LinearSVC_classifier.pickle', 'rb')
linearClassifier = pickle.load(linearDoc)
linearDoc.close()

sgdcDoc = open('SGDC_classifier.pickle', 'rb')
sgdcClassifier = pickle.load(sgdcDoc)
sgdcDoc.close()

word_features = pickle.load(open('features.pickle', 'rb'))
test_data = pickle.load(open('testing.pickle', 'rb'))
stopwords = set(stopwords.words('english'))

def find_features(document):
    temp_words = word_tokenize(document)
    words = []
    for w in temp_words:
        if w not in stopwords:
            processed_word = w.lower()
            words.append(processed_word)
    features= {}
    for w in word_features:
        features[w] = (w in words)
    return features

features = find_features("This movie was awesome! The acting was great, plot was wonderful, and there were pythons...so yea!")
features2 = find_features("This movie was utter junk. There were absolutely 0 pythons. I don't see what the point was at all. Horrible movie, 0/10")
# print features
# print features2
# sentiment = (bayesClassifier.classify(features))
# sentiment2 = (bayesClassifier.classify(features2))
# bayesClassifier.show_most_informative_features(15)
# print sentiment, sentiment2
# print nltk.classify.accuracy(bayesClassifier, test_data)

tweet_classifier = TweetClassifier(bayesClassifier, bayesClassifier2, mnbClassifier, sgdcClassifier, linearClassifier, logisticClassifier)

print tweet_classifier.classify(features), tweet_classifier.confidence(features)

print tweet_classifier.classify(features2), tweet_classifier.confidence(features2)