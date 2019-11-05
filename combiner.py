from os import walk
import json
import csv


def filter_json_files(filename):
    return 'message_1.json' in filename

def filter_jpg_files(filename):
    return '.jpg' in filename


# IMPORTANT ARRAY FUNCTIONS
# array = [1,2,3]
# odds = filter(isOdd, array) = [1,3]
# doubled = map(times2, array) = [2,4,6]
# summed = reduce(sum, array) = 6 (1+2+3)
def make_thread_key(message):
    participants = message['participants']
    # map, filter, and reduce
    # [{"name": "Zach Wilson"}, {"name": "Joann Vuong"}]
    # ["Zach Wilson", "Joann Vuong"]
    # Zach Wilson-Joann Vuong
    return '-'.join(list(map(lambda x: x['name'], participants)))


def map_messages(identifier, participants, message):
    message['thread_identifier'] = identifier
    message['participants'] = participants
    return message

class Combiner:
    def __init__(self, path="data/facebook/messages"):
        self.path = path
        print("created a new combiner with path " + self.path)

    def combine(self):
        print("combining files for path:" + self.path)
        all_json_files = []
        all_jpg_files = []
        # we want to walk the directory that we pass in from main.py (usually data/facebook/messages)
        for (path, directory, filenames) in walk(self.path):
            json_files = list(filter(filter_json_files, filenames))
            for file in json_files:
                all_json_files.append(path + '/' + file)

            jpg_files = list(filter(filter_jpg_files, filenames))
            for file in jpg_files:
                all_jpg_files.append(path + '/' + file)

        all_messages = []

        csv_file = csv.writer(open("data.csv", "w"))

        for file in all_json_files:
            with open(file) as f:
                j = json.load(f)
                participants = make_thread_key(j)
                identifier = j["thread_path"]
                messages = j["messages"]
                mapped_messages = list(
                    map(lambda message: map_messages(identifier, participants, message), messages)
                )
                all_messages.extend(mapped_messages)

        csv_file.writerow(["thread_identifier", "participants", "content", "timestamp_ms", "sender_name", "type"])
        for message in all_messages:
            if "content" in message:
                csv_file.writerow([message["thread_identifier"], message["participants"], message["content"], message["timestamp_ms"], message["sender_name"], message["type"]])
        return ["data.csv"]
