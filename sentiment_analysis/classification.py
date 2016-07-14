import nltk, pickle, random
from nltk.corpus import stopwords
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from nltk.tokenize import word_tokenize
import sys

reload(sys)
sys.setdefaultencoding('Latin-1')



positive_data = open('positive.txt', 'rb').read()
negative_data = open('negative.txt', 'rb').read()

all_words = []
documents = []

stopwords = set(stopwords.words('english'))

for sentence in positive_data.split("\n"):
    documents.append((sentence, 'pos'))
    words = word_tokenize(sentence)
    for w in words:
        if w not in stopwords:
            processed_word = w.lower()
            all_words.append(processed_word)



for sentence in negative_data.split("\n"):
    documents.append((sentence, 'neg'))
    words = word_tokenize(sentence)
    for w in words:
        if w not in stopwords:
            processed_word = w.lower()
            all_words.append(processed_word)

save_documents = open('documents.pickle', 'wb')
pickle.dump(documents, save_documents)
save_documents.close()

all_words = nltk.FreqDist(all_words)
print all_words

word_features = list(all_words.keys())[:5000]

save_word_features = open('features.pickle', 'wb')
pickle.dump(word_features, save_word_features)
save_word_features.close()

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

featuresets = [(find_features(rev), category) for (rev,category) in documents]

random.shuffle(featuresets)
print(featuresets)

testing_set = featuresets[10000:]
training_set = featuresets[:10000]

trainingFile = open('training.pickle', 'wb')
pickle.dump(training_set, trainingFile)
trainingFile.close()

testingFile = open('testing.pickle', 'wb')
pickle.dump(testing_set, testingFile)
testingFile.close()


classifier = nltk.NaiveBayesClassifier.train(training_set)
save_classifer = open('naivebayes2.pickle', 'wb')
pickle.dump(classifier, save_classifer)
save_classifer.close()

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
save_classifer = open('MNB_classifier.pickle', 'wb')
pickle.dump(classifier, save_classifer)
save_classifer.close()

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
save_classifer = open('Bernoulli_classifier.pickle', 'wb')
pickle.dump(classifier, save_classifer)
save_classifer.close()

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
save_classifer = open('LogisticRegression_classifier.pickle', 'wb')
pickle.dump(classifier, save_classifer)
save_classifer.close()

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
save_classifer = open('LinearSVC_classifier.pickle', 'wb')
pickle.dump(classifier, save_classifer)
save_classifer.close()

SGDC_classifier = SklearnClassifier(SGDClassifier())
SGDC_classifier.train(training_set)
save_classifer = open('SGDC_classifier.pickle', 'wb')
pickle.dump(classifier, save_classifer)
save_classifer.close()