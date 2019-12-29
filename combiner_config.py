from collections import namedtuple
import datetime as dt
import pytz

CombinerConfig = namedtuple("CombinerConfig", ["input_path",
                                               "output_directory", "output_file_name",
                                               "file_list", "output_columns", "file_to_rows"])


def map_messages(identifier, participants, message, timezone="America/Los_Angeles"):
    message['identifier'] = identifier
    message['participants'] = participants
    la_timezone = pytz.timezone(timezone)
    message['timestamp_iso'] = la_timezone.localize(dt.datetime.utcfromtimestamp(message['timestamp_ms']/1000)).isoformat()
    message['content'] = message['content'].replace('\n', ' ') if 'content' in message else ''
    return message


def message_file_to_rows(file, filename):
    participants = '-'.join(list(map(lambda x: x['name'], file["participants"])))
    identifier = file["thread_path"]
    messages = file["messages"]
    mapped_messages = list(
        map(lambda message: map_messages(identifier, participants, message), messages)
    )
    return mapped_messages


MessagesConfig = CombinerConfig(
    input_path="data/facebook/messages",
    output_directory='output',
    output_file_name="messages.csv",
    file_list=["message_1.json"],
    output_columns=[
            "identifier",
            "participants",
            "content",
            "timestamp_ms",
            "timestamp_iso",
            "sender_name",
            "type"
        ],
    file_to_rows=message_file_to_rows
)


def map_posts(message,  timezone="America/Los_Angeles"):
    message['identifier'] = message['timestamp']
    message['title'] = message['title'] if 'title' in message else 'Missing Title'
    la_timezone = pytz.timezone(timezone)
    message['timestamp_iso'] = la_timezone.localize(dt.datetime.utcfromtimestamp(message['timestamp'])).isoformat()
    for data in message['data'] if 'data' in message else []:
        if 'post' in data:
            message['content'] = data['post'].replace('\n', ' ')
    return message


def post_file_to_rows(file,filename):
    posts = file
    mapped_messages = list(
        map(lambda message: map_posts(message), posts)
    )
    return mapped_messages


PostsConfig = CombinerConfig(
    input_path="data/facebook/posts",
    output_directory='output',
    output_file_name="posts.csv",
    file_list=[
        "your_posts_" + str(x) + ".json" for x in range(1, 10)
    ],
    output_columns=[
            "identifier",
            "content",
            "timestamp",
            "timestamp_iso",
            "title"
    ],
    file_to_rows=post_file_to_rows
)


def map_locations(message, timezone="America/Los_Angeles"):
    message['identifier'] = message['creation_timestamp']
    message['longitude'] = message['coordinate']['longitude']
    message['latitude'] = message['coordinate']['latitude']
    message['title'] = message['title'] if 'title' in message else 'Missing Title'
    la_timezone = pytz.timezone(timezone)
    message['timestamp_iso'] = la_timezone.localize(dt.datetime.utcfromtimestamp(message['creation_timestamp'])).isoformat()

    return message


def location_file_to_rows(file, filename):
    locations = file['location_history']
    print(locations)
    mapped_messages = list(
        map(lambda message: map_locations(message), locations)
    )
    print(mapped_messages)
    return mapped_messages


LocationsConfig = CombinerConfig(
    input_path="data/facebook/location",
    output_directory='output',
    output_file_name="locations.csv",
    file_list=[
       "location_history.json"
    ],
    output_columns=[
            "identifier",
            "name",
            "creation_timestamp",
            "timestamp_iso",
            "longitude",
            "latitude"
    ],
    file_to_rows=location_file_to_rows
)


def map_likes(message, like_type, timezone="America/Los_Angeles"):
    message['identifier'] = message['timestamp']
    content_types = ['post', 'comment', 'photo', 'video', 'album', 'note', 'link', 'activity', 'GIF', 'life event']
    if like_type == 'reactions':
        valid_content_types = list(filter(lambda x: x in message['title'], content_types))
        message['title'] = message['title'] if 'title' in message else 'Missing Title'
        message['content_type'] = valid_content_types[0] if len(valid_content_types) > 0 else 'No valid content type'
        reaction_type = 'LIKE'
        for data in message['data']:
            if 'reaction' in data:
                reaction_type = data['reaction']['reaction']
        message['reaction_type'] = reaction_type
    if like_type == 'page':
        message['title'] = message['name'] if 'name' in message else 'Missing Title'
        message['content_type'] = 'page'
        message['reaction_type'] = 'LIKE'

    message['like_type'] = like_type
    la_timezone = pytz.timezone(timezone)
    message['timestamp_iso'] = la_timezone.localize(dt.datetime.utcfromtimestamp(message['timestamp'])).isoformat()

    return message


def likes_file_to_rows(file, filename):
    JSON_PARSE_KEY = {
        'pages.json': 'page_likes',
        'posts_and_comments.json': 'reactions'
    }
    LIKE_TYPE_DICT = {
        'pages.json': 'page',
        'posts_and_comments.json': 'reactions'
    }

    likes = file[JSON_PARSE_KEY[filename]]
    mapped_messages = list(
        map(lambda message: map_likes(message, LIKE_TYPE_DICT[filename]), likes)
    )
    print(mapped_messages)
    return mapped_messages


LikesConfig = CombinerConfig(
    input_path="data/facebook/likes_and_reactions",
    output_directory='output',
    output_file_name="likes_and_reactions.csv",
    file_list=[
       "posts_and_comments.json"
    ],
    output_columns=[
            "identifier",
            "like_type",
            "reaction_type",
            "content_type",
            "timestamp",
            "timestamp_iso",
            "title"
    ],
    file_to_rows=likes_file_to_rows
)

