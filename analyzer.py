import nltk

from nltk import word_tokenize, pos_tag, ne_chunk
import csv

# Analyzes the csv output from combiner.py and produces extracted entities
class Analyzer:
    def __init__(self, files):
        self.files = files
        # importing the different nltk packages for entity extraction
        nltk_packages = ['punkt','averaged_perceptron_tagger','maxent_ne_chunker', 'words']
        for package in nltk_packages:
            nltk.download(package)
        print("created a new analyzer")

    def analyze(self):
        print("analyzing files:" + str(self.files))
        for file in self.files:
            with open(file, encoding='utf-8', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if 'content' in row and 'participants' in row:
                        sentence = str(row['content'].encode('utf-8'))
                        entities = ne_chunk(pos_tag(word_tokenize(sentence)))
                        print(sentence)
                        print(entities)