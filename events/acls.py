import json
import requests 
from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY

def get_photo(city, state):
    headers = {"Authorization": PEXELS_API_KEY}
    
    params = {
        "per_page": 1,
        "query": f"{city} {state}"
    }
    
    url = "https://api.pexels.com/v1/search"
    
    response = requests.get(url, params=params, headers=headers)

    content = json.loads(response.content)
    
    try:
        return {"picture_url": content["photos"][0]["src"]["original"]}
    except (KeyError, IndexError):
        return {"picture_url": None}


def get_weather_data(city, state):

    url = "http://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": f"{city},{state}",
        "appid": OPEN_WEATHER_API_KEY
    }
    
    response = requests.get(url, params=params)
    content = json.loads(response.content)
    print(content)
    print("\n")
    latitude = content[0]['lat']
    longitude = content[0]['lon']


    weather_url = "https://api.openweathermap.org/data/2.5/weather"

    weather_params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPEN_WEATHER_API_KEY
    }

    response = requests.get(weather_url, weather_params=weather_params)
   
    weather_content = json.loads(response.weather_content)
    # print(weather_content)
    # print("\n")
    try:
        return {
            "weather": weather_content["main"][0]["temp"], 
            "description": weather_content["weather"][0]["description"]
            }
            
    except (KeyError, IndexError):
        return {"weather": None}


