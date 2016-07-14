import nltk
import random
import pickle
from nltk.corpus import movie_reviews

documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)
all_words = []
for w in movie_reviews.words():
    all_words.append(w.lower())
# print documents
all_words = nltk.FreqDist(all_words)
# print all_words

word_features = list(all_words.keys())[:3000]
#print word_features

def find_features(document):
    words = set(document)
    features= {}
    for w in word_features:
        features[w] = (w in words)
    return features

#print find_features(movie_reviews.words('neg/cv000_29416.txt'))

featuresets = [(find_features(rev), category) for (rev,category) in documents]

training_set = featuresets[:1900]
testing_set = featuresets[1900:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
#print nltk.classify.accuracy(classifier, testing_set)

save_classifer = open("naivebayes.pickle", 'wb')
pickle.dump(classifier, save_classifer)
save_classifer.close()

# classifier_f = open("naivebayes.pickle", 'rb')
# classifer = pickle.load(classifier_f)
# classifier_f.close()