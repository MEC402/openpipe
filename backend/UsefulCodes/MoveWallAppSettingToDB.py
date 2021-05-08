import json

def moveSetting():
    with open('dsAppSettings.json') as json_file:
        data = json.load(json_file)
        for key in data:
            print(key)

