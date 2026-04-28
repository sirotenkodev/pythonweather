import os
import json
import requests
import jinja2

def get_weather(settings):
    return requests.get(settings["baseurl"] + "?q=" + settings["city"] + "&appid=" + settings["appid"] + "&units=metric").json()

def load_setting():
    settings_file = "newsettings.json"
    os_name = os.name
    if os_name== 'nt':
        user = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
        settings = {}
        if os.access(user + "\\" + settings_file, os.R_OK):
            with open(user + "\\" + settings_file, 'r') as json_file:
                parser_data = json.load(json_file)
                settings["baseurl"] = parser_data['baseurl']
                settings["city"] = parser_data['city']
                settings["appid"] = parser_data['appid']
        return settings
    elif os_name == 'posix':
        home = os.path.expanduser('~')
        settings = {}
        if os.access(home + '/' + settings_file, os.R_OK):
            with open(home + '/' + settings_file, 'r') as json_file:
                parser_data = json.load(json_file)
                settings['baseurl'] = parser_data['baseurl']
                settings['city'] = parser_data['city']
                settings['appid'] = parser_data['appid']
        return settings

def save_setting(settings):
    settings_file = "newsettings.json"
    os_name = os.name
    if os_name == "nt":
        user = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
        with open(user + "\\" + settings_file, 'a') as json_file:
            json.dump(settings, json_file)
    elif os_name == 'posix':
        home = os.path.expanduser('~')
        with open(home + "/" + settings_file, 'a') as json_file:
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

weather = get_weather(settings)

envir = jinja2.Environment()
templateCity = envir.from_string("Погода в городе {{ city }}")
templateFeels = envir.from_string("Ощущается как {{ feels }}")
templateDescription = envir.from_string("Описание: {{ desc }}")

city = templateCity.render(city = weather["name"])
feels = templateFeels.render(feels = weather["main"]["feels_like"])
desc = templateDescription.render(desc = weather["weather"][0]["description"])

print(city)
print(feels)
print(desc)
