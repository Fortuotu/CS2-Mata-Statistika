import json

from scrape import try_get_skin_data

def write_json(obj, filename):
    with open(filename, 'w') as f:
        json.dump(obj, f)

def pretty_write_json(obj, filename):
   with open(filename, 'w') as f:
        json.dump(obj, f, indent=4)

def read_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}

def parse_skins(skins, skin_cache: dict = {}):
    if not skin_cache:
        skin_cache = read_json('json/skin_cache.json')

    parsed = {}

    for skin in skins:
        name = skin['Name']

        if name not in skin_cache:
            print(f'Getting skin data for {name}')

            data = try_get_skin_data(name)
            if not data:
                continue

            skin_cache[name] = data
            pretty_write_json(skin_cache, 'json/skin_cache.json')
            
        parsed[name] = skin_cache[name]
    
    return parsed

def parse_cases():
    data = read_json('json/latest.json')

    out = {}

    for case in data['Cases']:
        steam_market = case['MarketPlaces'][0]
        assert steam_market['Name'] == 'Steam'

        skins = parse_skins(steam_market['Skins'])

        """
        out[case['Name']] = {
            'name': case['Name'],
            'cost': case['Cost'],
            'key_cost': case['KeyCost'],
            'roi': steam_market['Average']['ROI'],
            'skins': skins
        }

        pretty_write_json(out, 'json/parsed.json')
        """

if __name__ == '__main__':
    parse_cases()
