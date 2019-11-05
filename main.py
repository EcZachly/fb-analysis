from combiner import Combiner
from analyzer import Analyzer

combiner = Combiner(path="data/facebook/messages")
files = combiner.combine()

analyzer = Analyzer(files=files)
analyzer.analyze()

