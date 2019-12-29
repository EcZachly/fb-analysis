import os
import json
import csv
from combiner_config import CombinerConfig


# creates a csv file from facebook directory
class Combiner:
    def __init__(self, config: CombinerConfig):
        self.input_path = config.input_path
        if not os.path.exists(config.output_directory):
            os.mkdir(config.output_directory)
        self.output_file_path = config.output_directory + '/' + config.output_file_name
        if os.path.exists(self.output_file_path):
            os.remove(self.output_file_path)
        self.file_list = config.file_list
        self.output_columns = config.output_columns
        self.file_to_rows = config.file_to_rows
        print("created a new combiner with path " + self.input_path)

    def combine(self):
        print("combining files for path:" + self.input_path)
        all_files = []
        # we want to walk the directory that we pass in from main.py (usually data/facebook/messages)
        for (path, directory, filenames) in os.walk(self.input_path):
            print(filenames)
            print(self.file_list)
            json_files = list(filter(lambda file_name: file_name in self.file_list, filenames))
            for file in json_files:
                all_files.append(path + '/' + file)

        all_rows = self.process_files(all_files)
        file_name = self.write_csv_file(all_rows, self.output_file_path, self.output_columns)
        return file_name

    def process_files(self, files):
        all_messages = []
        for file in files:
            with open(file) as f:
                json_file = json.load(f)
                mapped_messages = self.file_to_rows(json_file, os.path.basename(f.name))
                all_messages.extend(mapped_messages)
        return all_messages

    @classmethod
    def write_csv_file(cls, messages, filename, output_columns):
        csv_file = csv.writer(open(filename, mode="w", encoding='utf-8', newline='\n'))
        csv_file.writerow(output_columns)
        for message in messages:
            output_message = list(map(lambda col: message[col], output_columns))
            csv_file.writerow(output_message)
        return filename

