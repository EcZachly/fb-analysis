import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def process_message_entities(entities):
    contains_gpe = False
    contains_person = False
    contains_organization = False
    contains_trump = False
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
        return [contains_gpe, contains_person, contains_organization, contains_trump]
# Analyzes the csv output from combiner.py and produces extracted entities
class Analyzer:
    def __init__(self, file):
        self.input_file = file
        self.output_file_name = 'data_with_scores.csv'
        self.output_directory = 'output'
        self.content_index = 2
        self.process_entities = process_message_entities
        self.min_num_columns = 3
        self.output_columns = ["thread_identifier", "participants", "content", "timestamp_ms", "timestamp_iso",
                               "sender_name", "type", "positive_value", "negative_value", "neutral_value",
                               "compound_value", "contains_person", "contains_gpe", "contains_organization",
                               "contains_trump"]
        # importing the different nltk packages for entity extraction
        nltk_packages = ['vader_lexicon','stopwords','punkt','averaged_perceptron_tagger','maxent_ne_chunker', 'words']
        for package in nltk_packages:
            nltk.download(package)
        print("created a new analyzer")

    def analyze(self):
        print("analyzing files:" + str(self.input_file))
        with open(self.input_file, encoding='utf-8', mode='r') as csv_file:
            with open(self.output_directory + '/' + self.output_file_name, newline='\n', encoding='utf-8', mode='w') as output_file:
                csv_writer = csv.writer(output_file)
                csv_writer.writerow(self.output_columns)
                csv_reader = csv.reader(csv_file)
                next(csv_reader)
                sid = SentimentIntensityAnalyzer()
                for row in csv_reader:
                    content = None
                    if len(row) > self.min_num_columns:
                        content = row[self.content_index]
                    if content is not None:
                        sentence = str(content.encode('utf-8'))
                        sentiment_score = sid.polarity_scores(sentence)
                        print(sentiment_score)
                        print(sentence)
                        positive_value = sentiment_score['pos']
                        negative_value = sentiment_score['neg']
                        neutral_value = sentiment_score['neu']
                        compound_value = sentiment_score['compound']
                        entities = ne_chunk(pos_tag(word_tokenize(sentence)))
                        processed_columns = self.process_entities(entities)
                        csv_writer.writerow(row + [positive_value, negative_value, neutral_value, compound_value] + processed_columns)

