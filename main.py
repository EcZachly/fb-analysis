from combiner import Combiner
from analyzer import Analyzer

combiner = Combiner()
files = combiner.combine()

analyzer = Analyzer(files=files)
analyzer.analyze()

