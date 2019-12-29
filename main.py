from combiner import Combiner
from analyzer import Analyzer
from combiner_config import MessagesConfig, PostsConfig, LocationsConfig, LikesConfig

combiner = Combiner(config=MessagesConfig)
files = combiner.combine()


analyzer = Analyzer(files=['data.csv'])
analyzer.analyze()

