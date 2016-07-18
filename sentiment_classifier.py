import os
import time
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report, accuracy_score



class SentimentClassifier():

    def __init__(self):
        STOP_WORD_FILE = os.path.join('polarityData', 'english.txt')
        self.stopset = open(STOP_WORD_FILE,'r').read().split()
        self.stopset += ['t', 'AT_USER', 'STOCK', 'URL', 'RT']
        self.stopset.remove('above')
        self.stopset.remove('below')
        self.stopset.remove('under')
        self.stopset.remove('up')
        self.stopset.remove('down')
        self.vectorizer = TfidfVectorizer(min_df=5, max_df=0.8, sublinear_tf=True, use_idf=True, ngram_range=(2, 2))
        self.classifier = self.evaluate_classifier()

    def process_sentence(self,tweet):
            tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
            tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
            tweet = re.sub('\$[^\s]+', 'STOCK', tweet)
            tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
            return tweet

    def process_tweet(self, tweet):
        feature_words = []
        tweet = self.process_sentence(tweet)
        tweet = re.findall(r"[A-Za-z]+", tweet.rstrip())
        for word in tweet:
            if word not in self.stopset:
                feature_words.append(word.lower())
        sentence = ' '.join(feature_words)
        return sentence


    def classify_tweet(self,tweet):
        feature_words = []
        tweet = self.process_sentence(tweet)
        tweet = re.findall(r"[A-Za-z]+", tweet.rstrip())
        for word in tweet:
            if word not in self.stopset:
                feature_words.append(word.lower())
        sentence = ' '.join(feature_words)
        sentiment = self.classifier.predict(self.vectorizer.transform([sentence]))
        return sentiment

    def evaluate_classifier(self):
        classes = ['pos', 'neg']
        train_data = []
        train_labels = []
        test_data = []
        test_labels = []
        RT_POLARITY_POS_FILE = os.path.join('polarityData', 'positive.txt')
        RT_POLARITY_NEG_FILE = os.path.join('polarityData', 'negative.txt')

        with open(RT_POLARITY_POS_FILE, 'r') as posSentences:
            for line in posSentences:
                line = self.process_tweet(line)
                train_data.append(line)
                train_labels.append(classes[0])

        with open(RT_POLARITY_NEG_FILE, 'r') as negSentences:
            for line in negSentences:
                line = self.process_tweet(line)
                train_data.append(line)
                train_labels.append(classes[1])
        train_vectors = self.vectorizer.fit_transform(train_data)
        test_vectors = self.vectorizer.transform(train_data)
        classifier_liblinear = svm.LinearSVC()
        t0 = time.time()
        classifier_liblinear.fit(train_vectors, train_labels)
        t1 = time.time()
        prediction_liblinear = classifier_liblinear.predict(train_vectors)
        t2 = time.time()
        time_liblinear_train = t1 - t0
        time_liblinear_predict = t2 - t1
        accuracy_score3 = accuracy_score(train_labels, prediction_liblinear)
        print(accuracy_score3)
        return classifier_liblinear


if __name__ == '__main__':
    sentClassifier = SentimentClassifier()
    print(sentClassifier.classify_tweet("Williams Cos. downgraded by  Investment Research to hold"))