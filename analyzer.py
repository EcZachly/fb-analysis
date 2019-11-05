class Analyzer:
    def __init__(self, files):
        self.files = files
        print("created a new analyzer")

    def analyze(self):
        print("analyzing files:" + str(self.files))