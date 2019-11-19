import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

from nltk import word_tokenize, pos_tag, ne_chunk
import csv
class Analyzer:
    def __init__(self, files):
        self.files = files
        print("created a new analyzer")

    def analyze(self):
        print("analyzing files:" + str(self.files))
        for file in self.files:
            with open(file, encoding='utf-8', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                sentences = str("")
                for row in csv_reader:
                    if 'content' in row and 'participants' in row and row['participants'] == 'Zach Wilson-JoAnn Vuong':
                        sentences += " . " + str(row['content'].encode('utf-8'))
                entities = ne_chunk(pos_tag(word_tokenize(sentences)))
                print(sentences)