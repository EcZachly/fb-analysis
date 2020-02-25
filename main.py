from combiner import Combiner
from analyzer import Analyzer
from combiner_config import MessagesConfig, PostsConfig, LocationsConfig, LikesConfig, CommentsConfig
from analyzer_config import MessagesAnalyzerConfig, CommentsAnalyzerConfig, PostsAnalyzerConfig
combiner = Combiner(config=PostsConfig)
files = combiner.combine()


analyzer = Analyzer(config=PostsAnalyzerConfig)
analyzer.analyze()

