import nltk
import string
import re
import csv
def deEmojify(inputString):
    emoji_pattern = re.compile(
        u"(\ud83d[\ude00-\ude4f])|"  # emoticons
        u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
        u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
        "+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', inputString)  # no emoji
def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase
#nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
filename = 'twitDB_sarcasm.csv'
output_filename = 'cleanedtweets.csv'
badcharacters = ['#','@']
with open(filename, encoding='utf-8', mode='r') as csv_file: #reading in the file
    output_file = csv.writer(open(output_filename, mode="w", encoding='utf-8', newline='\n'))
    data = '   '
    while len(data) > 0:
        data = csv_file.readline()
        data = deEmojify(decontracted(data.lower())) #making all of the words lowercase in order to standardize our data
        words = data.split()
        filtered_words = []
        for word in words:
            contains_badcharacter = False #assume each word doesn't have a hashtag in it
            for badcharacter in badcharacters:
                if badcharacter in word:
                    contains_badcharacter = True
            filtered_word = word.translate(str.maketrans('', '', string.punctuation))
            if filtered_word not in stopwords and not contains_badcharacter:
                filtered_words.append(filtered_word)

        print(words)
        print(filtered_words)
        if len(filtered_words) >= 2:
            row = ' '.join(filtered_words) #join changes back into strings
            output_file.writerow([row, 1])
