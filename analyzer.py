import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
import csv
from analyzer_config import AnalyzerConfig
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Analyzes the csv output from combiner.py and produces extracted entities
class Analyzer:
    def __init__(self, config: AnalyzerConfig):
        self.input_file = config.input_file
        self.output_file_name = config.output_file_name
        self.output_directory = config.output_directory
        self.content_index = config.content_index
        self.process_entities = config.process_entities
        self.min_num_columns = config.min_num_columns
        self.output_columns = config.output_columns
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

