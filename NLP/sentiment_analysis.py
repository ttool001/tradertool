import csv, nltk, re

STOP_WORDS = []
def process_tweet(tweet):
    """
    Processes tweets to make lower case and remove @user and # for hashtags
    :param tweet:
    :return:
    """

    tweet = tweet.lower()

    # from www or https to URL

    tweet = re.sub('((www\.[^\s])|(https?://[^\s]+))', 'URL', tweet)

    #
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)

    tweet = re.sub('[\s]+', ' ', tweet)

    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

    tweet = tweet.strip('\'"')
    return tweet

def replace_repeat_letters(tweet):
    """
    Replaces repeating letters
    :param tweet:String:tweet for processing
    :return:String:tweet after process
    """
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", tweet)


def get_stop_words(filename):
    """
    Returns a list of stop words to process tweet
    :param filename: String: filename that stores common stop words
    :return: [string] list of strings
    """
    stop_word_list = []
    stop_word_list.append('AT_USER')
    stop_word_list.append('URL')
    stop_word_list.append('rt')
    stop_file = open(filename, 'r')
    line = stop_file.readline()
    while line:
        word = line.strip()
        stop_word_list.append(word)
        line = stop_file.readline()
    stop_file.close()
    return stop_word_list


def get_features_from_tweet(tweet):
    feature_vector = []
    words = tweet.split()
    for word in words:
        word = replace_repeat_letters(word)

        word = word.strip('\"?,*.')
        #print word
        word_alpha = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", word)
        if (word in STOP_WORDS) or (word_alpha is None):
            continue
        else:
           if word != "rt":
                feature_vector.append(word.lower())
    return feature_vector

def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in tweet_words:
        features['contains(%s)' % word] = (word in tweet_words)
    return features



def main():
    featureList = []
    tweet_classifier_features = []
    tweets = open("Sentiment.csv",'r' )
    tweet_reader = csv.reader(tweets)
    tweet_reader.next()
    STOP_WORDS = get_stop_words("stopWords.txt")
    #print STOP_WORDS
    for line in tweet_reader:
        sentiment = line[5]
        tweet = line[15]
        processed_tweet = process_tweet(tweet)
        feature_vector = get_features_from_tweet(processed_tweet)
        featureList.extend(feature_vector)
        tweet_classifier_features.append((feature_vector,sentiment))

    featureList = list(set(featureList))
    training_set = nltk.classify.util.apply_features(extract_features, tweet_classifier_features)

    test_tweet = "One year ago @SenSanders announced his run for presidency  thank you for giving us hope Bernie #Still Sanders #Bernie O rBust #Bernie Sanders"
    test_tweet2 = "I can't wait to see how these vulgar, cursing, child, dreamers and #BernieSanders supporters, end up as adults"

    #naiveBayes = nltk.NaiveBayesClassifier.train(training_set)
    maximumEntropy = nltk.MaxentClassifier.train(training_set, max_iter = 10)
    #print training_set
    #print naiveBayes.classify(extract_features(process_tweet(test_tweet)))
    #print naiveBayes.classify(extract_features(process_tweet(test_tweet2)))
    #print naiveBayes.show_most_informative_features(10)
    print maximumEntropy.classify(extract_features(process_tweet(test_tweet2)))
    tweets.close()

if __name__ == '__main__':
    main()