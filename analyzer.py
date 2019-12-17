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
                with open('data_with_entities.csv', encoding='utf-8', mode='w') as output_file:
                    csv_writer = csv.writer(output_file)
                    csv_reader = csv.reader(csv_file)
                    csv_writer.writerow(["thread_identifier", "participants", "content", "timestamp_ms", "sender_name", "type", "entity_name", "entity_label"])
                    for row in csv_reader:
                        if len(row) > 3:
                            content = row[2]
                            participants = row[1]
                        if content is not None and participants is not None:
                            sentence = str(content.encode('utf-8'))
                            entities = ne_chunk(pos_tag(word_tokenize(sentence)))
                            for entity in entities:
                                if type(entity) != type(()):
                                    entity_name = ""
                                    for leaf in entity.leaves():
                                        entity_name += leaf[0] + ' '
                                    entity_name = entity_name.strip()
                                    entity_label = entity.label()
                                    csv_writer.writerow(row + [entity_name, entity_label])