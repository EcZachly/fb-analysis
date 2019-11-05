import json

def read_example_file():
    with open('data/example/example.json') as f:
        jsondata = json.load(f)
        options = jsondata['options']
        parser = options['parser']
        if 'decodeEntities' in parser:
            print(parser['decodeEntities'])
        else:
            print('parser did not work')

def read_pokemon_file():
    with open('data/example/pokemon.json') as f:
        jsondata = json.load(f)
        name = jsondata['name']
        stats = jsondata['stats']
        highvalue = 0
        lowvalue = 9000
        highname = ""
        lowname = ""

        for stat in stats:
            basestat = stat['base_stat']
            statname = stat['stat']['name']
            if basestat >= highvalue:
                highvalue = basestat
                highname = statname
            if basestat < lowvalue:
                lowvalue = basestat
                lowname = statname
        print(name + ' lowest stat is ' + lowname + ' with the value of ' + str(lowvalue))
        print(name + ' highest stat is ' + highname + ' with the value of ' + str(highvalue))

read_pokemon_file()