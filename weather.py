import os
import json
import requests

def get_weather(settings):
    return requests.get(settings["baseurl"] + "?q=" + settings["city"] + "&appid=" + settings["appid"]).json()

def load_setting():
    settings_file = "newsettings.json"
    user = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
    settings = {}
    if os.access(user + "\\" + settings_file, os.R_OK):
        with open(user + "\\" + settings_file, 'r') as json_file:
            parser_data = json.load(json_file)
            settings["baseurl"] = parser_data['baseurl']
            settings["city"] = parser_data['city']
            settings["appid"] = parser_data['appid']
    return settings

def save_setting(settings):
    settings_file = "newsettings.json"
    user = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
    with open(user + "\\" + settings_file, 'a') as json_file:
        json.dump(settings, json_file)

def input_setting():
    settings = {}
    settings["baseurl"] = "https://api.openweathermap.org/data/2.5/weather"
    settings["city"] = input("Enter your city here: ")
    settings["appid"] = input("Enter your API key here: ")
    save_setting(settings)
    return settings



settings = load_setting()
if not settings:
    settings = input_setting()

print(get_weather(settings))




