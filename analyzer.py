import pandas as pd
import numpy as np
class Analyzer:
    def __init__(self, files):
        self.files = files
        print("created a new analyzer")

    def analyze(self):
        print("analyzing files:" + str(self.files))
        for file in self.files:
            dataframe = pd.read_csv(file)
            senders = dataframe.groupby('sender_name') # Grouping by sender_name
            print(senders['sender_name'].count().sort_values(ascending=False)) # Using Sender from line 12 and counts the number of messages each sender sends
            