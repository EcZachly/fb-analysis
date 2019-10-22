import json

with open('data/example/example.json') as f:
    jsondata = json.load(f)
    options = jsondata['options']
    parser = options['parser']
    if 'decodeEntities' in parser:
        print(parser['decodeEntities'])
    else:
        print('parser did not work')
