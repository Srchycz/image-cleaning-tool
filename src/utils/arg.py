import json

def parse_args():
    with open('../config/settings.json') as f:
        args = json.load(f)
    return args