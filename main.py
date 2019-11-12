from combiner import Combiner
from analyzer import Analyzer

#combiner = Combiner(path="data/facebook/messages/inbox")
#files = combiner.combine()

analyzer = Analyzer(files=['data.csv'])
analyzer.analyze()

