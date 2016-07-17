from nltk import precision
from nltk import recall
import nltk.util
import re
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews, stopwords
from nltk import BigramAssocMeasures, BigramCollocationFinder

import os, collections, pickle, itertools

RT_POLARITY_POS_FILE = os.path.join('polarityData', 'positive.txt')
RT_POLARITY_NEG_FILE = os.path.join('polarityData', 'negative.txt')




class StockSentiAnalyzer():

    def __init__(self):
        self.stopset = list(stopwords.words('english'))
        self.stopset += ['t', 'AT_USER', 'STOCK', 'URL', 'RT']
        self.stopset.remove('above')
        self.stopset.remove('below')
        self.stopset.remove('under')
        self.stopset.remove('up')
        self.stopset.remove('down')
        self.best_words = self.find_best_features()
        self.classifier = self.evaluate_classifier(self.best_bigram_word_feats)


    def evaluate_classifier(self, feature_extractor):
        featx = feature_extractor

        posWords = []
        negWords = []

        with open(RT_POLARITY_POS_FILE, 'r') as posSentences:
            for i in posSentences:
                posWord = self.process_tweet(i)
                posWords.append(posWord)

        with open(RT_POLARITY_POS_FILE, 'r') as posSentences:
            for i in posSentences:
                negWord = self.process_tweet(i)
                negWords.append(negWord)

        negfeats = [(featx(neg_sen), 'neg') for neg_sen in negWords ]
        posfeats = [(featx(pos_sen), 'pos') for pos_sen in posWords ]
        negcutoff = int(len(negfeats) * 9 / 10)
        poscutoff = int(len(posfeats) * 9 / 10)

        trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
        testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

        classifier = NaiveBayesClassifier.train(trainfeats)
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)

        for i, (feats, label) in enumerate(testfeats):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)

        # classifier_file = open('naivebayes.pickle', 'wb')
        # pickle.dump(classifier, classifier_file)
        print('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
        classifier.show_most_informative_features()
        return classifier

    def find_best_features(self):
        posWords = []
        negWords = []

        with open(RT_POLARITY_POS_FILE, 'r') as posSentences:
            for i in posSentences:
                tweet = self.process_sentence(i)
                posWord = re.findall(r"[A-Za-z]+", tweet.rstrip())
                posWords.append(posWord)

        with open(RT_POLARITY_POS_FILE, 'r') as posSentences:
            for i in posSentences:
                tweet = self.process_sentence(i)
                negWord = re.findall(r"[A-Za-z]+", tweet.rstrip())
                negWords.append(negWord)
        word_fd = nltk.FreqDist()
        label_word_fd = nltk.ConditionalFreqDist()

        posWords = list(itertools.chain(*posWords))
        negWords = list(itertools.chain(*negWords))
        for pos_word in posWords:
            if pos_word not in self.stopset:
                word_fd[pos_word.lower()] += 1
                label_word_fd['pos'][pos_word.lower()] += 1
        for neg_word in negWords:
            if neg_word not in self.stopset:
                word_fd[neg_word.lower()] += 1
                label_word_fd['neg'][neg_word.lower()] += 1
        pos_word_count = label_word_fd['pos'].N()
        neg_word_count = label_word_fd['neg'].N()
        total_word_count = pos_word_count + neg_word_count

        word_scores = {}

        for word, freq in word_fd.items():
            pos_score = BigramAssocMeasures.chi_sq(label_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
            neg_score = BigramAssocMeasures.chi_sq(label_word_fd['neg'][word], (freq, neg_word_count),total_word_count)
            word_scores[word] = pos_score + neg_score
        best = sorted(word_scores.items(), key = lambda w:w[1], reverse=True)[:500]
        best_words = set([w for w , s in best])
        return best_words

    def best_word_features(self,words):
        return dict([(word, True) for word in words if word in self.best_words])

    def best_bigram_word_feats(self,words, score_fn=BigramAssocMeasures.chi_sq, n=10):
        bigram_finder = BigramCollocationFinder.from_words(words)
        bigrams = bigram_finder.nbest(score_fn, n)
        d = dict([(bigram, True) for bigram in bigrams])
        d.update(self.best_word_features(words))
        return d

    def process_sentence(self, tweet):
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
        tweet = re.sub('\$[^\s]+', 'STOCK', tweet)
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        return tweet


    def classify_tweet(self, tweet):
        feature_words = []
        feature_words = self.process_tweet(tweet)
        features = self.best_bigram_word_feats(feature_words)
        print (self.classifier.classify(features))

    def process_tweet(self, tweet):
        feature_words = []
        tweet = self.process_sentence(tweet)
        tweet = re.findall(r"[A-Za-z]+", tweet.rstrip())
        for word in tweet:
            if word not in self.stopset:
                feature_words.append(word.lower())
        return feature_words


if __name__ == '__main__':
    # print(len(stopset))
    analyzer = StockSentiAnalyzer()
    #classifier_file = open('naivebayes.pickle', 'wb')
    #pickle.dump(analyzer.classifier, classifier_file)
    #classifier_file.close()
    #classifier_file = open('naivebayes.pickle', 'rb')
    # analyzer = pickle.load(classifier_file)
    sentence6 = "$IBM IV decreasing into quarterly results https://t.co/OoyrMd7sh5"
    analyzer.classify_tweet(sentence6)
