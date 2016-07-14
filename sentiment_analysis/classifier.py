import nltk, pickle, random
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

class TweetClassifier(ClassifierI):

    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for classifier in self._classifiers:
            v = classifier.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for classifier in self._classifiers:
            v = classifier.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        confidence_val = choice_votes/ len(votes)
        return confidence_val
