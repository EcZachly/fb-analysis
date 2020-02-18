from combiner import Combiner
from analyzer import Analyzer
from combiner_config import MessagesConfig, PostsConfig, LocationsConfig, LikesConfig

# combiner = Combiner(config=LikesConfig)
# files = combiner.combine()


analyzer = Analyzer(file='output/messages.csv')
analyzer.analyze()

