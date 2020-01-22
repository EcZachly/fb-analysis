import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Analyzes the csv output from combiner.py and produces extracted entities
class Analyzer:
    def __init__(self, files):
        self.files = files
        # importing the different nltk packages for entity extraction
        nltk_packages = ['vader_lexicon','stopwords','punkt','averaged_perceptron_tagger','maxent_ne_chunker', 'words']
        for package in nltk_packages:
            nltk.download(package)
        print("created a new analyzer")

    def analyze(self):
        stop_words = list(set(stopwords.words('english'))) #this is the list of common words
        print("analyzing files:" + str(self.files))
        for file in self.files:
            with open(file, encoding='utf-8', mode='r') as csv_file:
                with open('data_with_scores.csv', newline='\n', encoding='utf-8', mode='w') as output_file:
                    csv_writer = csv.writer(output_file)
                    csv_reader = csv.reader(csv_file)
                    csv_writer.writerow(["thread_identifier", "participants", "content", "timestamp_ms", "timestamp_iso", "sender_name", "type", "positive_value", "negative_value", "neutral_value", "compound_value","contains_person","contains_gpe","contains_organization","contains_trump"])
                    sid = SentimentIntensityAnalyzer()
                    for row in csv_reader:
                        if len(row) > 3:
                            content = row[2]
                            participants = row[1]
                        if content is not None and participants is not None:
                            sentence = str(content.encode('utf-8'))
                            sentiment_score = sid.polarity_scores(sentence)
                            print(sentiment_score)
                            print(sentence)
                            positive_value = sentiment_score['pos']
                            negative_value = sentiment_score['neg']
                            neutral_value = sentiment_score['neu']
                            compound_value = sentiment_score['compound']

                            contains_gpe = False
                            contains_person = False
                            contains_organization = False
                            contains_trump = False
                            entities = ne_chunk(pos_tag(word_tokenize(sentence)))
                            for entity in entities:
                                if type(entity) != type(()):
                                    entity_name = ""
                                    for leaf in entity.leaves():
                                        entity_name += leaf[0] + ' '
                                    entity_name = entity_name.strip()
                                    entity_label = entity.label()
                                    if entity_label == 'GPE':
                                        contains_gpe = True
                                    if entity_label == 'PERSON':
                                        contains_person = True
                                    if entity_label == 'ORGANIZATION':
                                        contains_organization = True
                                    if entity_name.lower() == 'trump':
                                        contains_trump = True
                            csv_writer.writerow(row + [positive_value, negative_value, neutral_value, compound_value,contains_gpe, contains_person, contains_organization,contains_trump])

