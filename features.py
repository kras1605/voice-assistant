import datetime
import subprocess
import webbrowser
import requests
import wikipedia
import nltk
import wolframalpha
import psutil
import pyjokes
import pyautogui
import math
import random
import json
import re
import geocoder
import string
import config
import pygame
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from geopy.geocoders import Nominatim
from geopy.distance import great_circle

class PygameImageHandler:
    def __init__(self):
        self.pics = dict()

    def loadFromFile(self, filename, id=None):
        if id == None:
            id = filename
        self.pics[id] = pygame.image.load(filename).convert()

    def loadFromSurface(self, surface, id):
        self.pics[id] = surface.convert_alpha()

    def render(self, surface, id, position=None, clear=False, size=None):
        if clear == True:
            surface.fill((5, 2, 23))

        if position == None:
            picX = int(surface.get_width() / 2 - self.pics[id].get_width() / 2)
        else:
            picX = position[0]
            picY = position[1]

        if size == None:
            surface.blit(self.pics[id], (picX, picY))

        else:
            surface.blit(pygame.transform.smoothscale(
                self.pics[id], size), (picX, picY))


def split_into_sentences(text):
    return nltk.tokenize.sent_tokenize(text)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

# =========================================== Main Functions ============================================


WEATHER_API_KEY = config.weather_api_key
NEWS_API_KEY = config.news_api_key

def get_day():
    day = datetime.datetime.today().weekday() + 1
    day_dictionary = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
                      4: 'Thursday', 5: 'Friday', 6: 'Saturday',
                      7: 'Sunday'}
    return day_dictionary[day]


def get_print_light_purple(text):
    print("\033[94m{}\033[00m" .format(text.title()))


def get_print_purple(text):
    print("\033[95m{}\033[00m" .format(text.title()))


def get_print_red(text):
    print("\033[91m{}\033[00m" .format(text.title()))


def get_print_cyan(text):
    print("\033[96m{}\033[00m" .format(text.title()))


def get_wish():
    try:
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour <= 12:
            wish = "Good Morning"
        elif hour > 12 and hour < 18:
            wish = "Good afternoon"
        else:
            wish = "Good evening"
        return wish
    except Exception as e:
        print(e)
        return False


def get_joke():
    try:
        return pyjokes.get_joke()
    except Exception as e:
        print(e)
        return False


def get_date():
    try:
        date = datetime.datetime.now().strftime("%b %d %Y")
    except Exception as e:
        print(e)
        date = False
    return date


def get_time():
    try:
        time = datetime.datetime.now().strftime("%H:%M:%S")
    except Exception as e:
        print(e)
        time = False
    return time


def get_app_launch(app_path):
    try:
        subprocess.call([app_path])
        return True
    except Exception as e:
        print(e)
        return False


def get_open_website(url):
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(e)
        return False


def get_wiki_response(topic):
    try:
        return wikipedia.summary(topic, sentences=3)
    except Exception as e:
        print(e)
        return False


def get_weather(city):
    try:
        res = ""
        units_format = "&units=metric"
        base_url = "http://api.openweathermap.org/data/2.5/weather?q="
        complete_url = base_url + city + "&appid=" + WEATHER_API_KEY + units_format
        response = requests.get(complete_url)
        city_weather_data = response.json()

        if city_weather_data["cod"] != "404":
            main_data = city_weather_data["main"]
            weather_description_data = city_weather_data["weather"][0]
            weather_description = weather_description_data["description"]
            current_temperature = main_data["temp"]
            current_pressure = main_data["pressure"]
            current_humidity = main_data["humidity"]
            wind_data = city_weather_data["wind"]
            wind_speed = wind_data["speed"]

            res = f"""
            The weather in {city} is currently {weather_description} 
            with a temperature of {current_temperature} degree celcius, 
            atmospheric pressure of {current_pressure} hectoPascals, 
            humidity of {current_humidity} percent 
            and wind speed reaching {wind_speed} kilometers per hour"""
        else:
            res = "Sorry Sir, I couldn't find the city in my database. Please try again"
    except Exception as e:
        print(e)
        res = False
    return res


def get_system_stats():
    cpu_stats = str(psutil.cpu_percent())
    battery_percent = psutil.sensors_battery().percent
    memory_in_use = convert_size(psutil.virtual_memory().used)
    total_memory = convert_size(psutil.virtual_memory().total)
    final_res = f"Currently {cpu_stats} percent of CPU, {memory_in_use} of RAM out of total {total_memory}  is being used and battery level is at {battery_percent} percent"
    return final_res


def get_google_search(command):
    reg_ex = re.search('search google for (.*)', command)
    search_for = command.split("for", 1)[1]
    url = 'https://www.google.com/'
    if reg_ex:
        subgoogle = reg_ex.group(1)
        url = url + 'r/' + subgoogle
    driver = webdriver.Chrome(
        executable_path='chrome_driver.exe')
    driver.get('https://www.google.com')
    search = driver.find_element_by_name('q')
    search.send_keys(str(search_for))
    search.send_keys(Keys.RETURN)


def get_location(place):
    webbrowser.open("http://www.google.com/maps/place/" + place + "")
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(place, addressdetails=True)
    target_latlng = location.latitude, location.longitude
    location = location.raw['address']
    target_loc = {'city': location.get('city', ''),
                  'state': location.get('state', ''),
                  'country': location.get('country', '')}

    current_loc = geocoder.ip('me')
    current_latlng = current_loc.latlng

    distance = str(great_circle(current_latlng, target_latlng))
    distance = str(distance.split(' ', 1)[0])
    distance = round(float(distance), 2)

    return current_loc, target_loc, distance


def get_my_location():
    ip_add = requests.get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_requests = requests.get(url)
    geo_data = geo_requests.json()
    city = geo_data['city']
    state = geo_data['region']
    country = geo_data['country']

    return city, state, country


def get_news():
    try:
        url = 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=' + NEWS_API_KEY
        news = requests.get(url).text
        news_dict = json.loads(news)
        articles = news_dict['articles']
        return articles
    except:
        return False


def take_screenshot():
    try:
        image = pyautogui.screenshot()
        image.save('screenshot - {}.png'.format(''.join(random.choices(string.ascii_lowercase +string.digits, k=6))))
        return "screenshot saved"
    except Exception as e:
        print(e)
        return False


def system_exit():
    try:
        sys.exit()
        return
    except Exception as e:
        print(e)
        return False
    

def get_my_ip():
    try:
        return "sir your ip adress is" + requests.get('https://api.ipify.org').text
    except Exception as e:
        print(e)
        return False
