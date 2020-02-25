from collections import namedtuple

AnalyzerConfig = namedtuple("AnalyzerConfig", ["input_file",
                                               "output_file_name",
                                               "output_directory", "content_index", "process_entities","min_num_columns","output_columns"])

def process_message_entities(entities):
    contains_gpe = False
    contains_person = False
    contains_organization = False
    contains_trump = False
    for entity in entities:
        if type(entity) != type(()):
            entity_name = ""
            for leaf in entity.leaves():
                entity_name += leaf[0] + ' '
            entity_name = entity_name.strip()
            entity_label = entity.label()
            if entity_label == 'GPE':
                contains_gpe = True
            if entity_label == 'PERSON':
                contains_person = True
            if entity_label == 'ORGANIZATION':
                contains_organization = True
            if entity_name.lower() == 'trump':
                contains_trump = True
        return [contains_gpe, contains_person, contains_organization, contains_trump]

MessagesAnalyzerConfig = AnalyzerConfig(
    input_file="output/messages.csv",
    output_file_name="messages_with_scores.csv",
    output_directory="output",
    content_index=2,
    process_entities=process_message_entities,
    min_num_columns=3,
    output_columns=["thread_identifier", "participants", "content", "timestamp_ms", "timestamp_iso",
                               "sender_name", "type", "positive_value", "negative_value", "neutral_value",
                               "compound_value", "contains_person", "contains_gpe", "contains_organization",
                               "contains_trump"]
)

CommentsAnalyzerConfig = AnalyzerConfig(
    input_file="output/comments.csv",
    output_file_name="comments_with_scores.csv",
    output_directory="output",
    content_index=2,
    process_entities=process_message_entities,
    min_num_columns=3,
    output_columns=["timestamp","title","content","author","timestamp_iso","positive_value", "negative_value", "neutral_value",
                               "compound_value", "contains_person", "contains_gpe", "contains_organization",
                               "contains_trump"]

)

PostsAnalyzerConfig = AnalyzerConfig(
    input_file="output/posts.csv",
    output_file_name="posts_with_scores.csv",
    output_directory="output",
    content_index=1,
    process_entities=process_message_entities,
    min_num_columns=3,
    output_columns=["identifier","content","timestamp","timestamp_iso","title","positive_value", "negative_value", "neutral_value",
                               "compound_value", "contains_person", "contains_gpe", "contains_organization",
                               "contains_trump"]

)