import requests
import os
from collections import namedtuple
from dotenv import load_dotenv

load_dotenv('weather_project/.env')

Image = namedtuple('Image', ['link', 'width', 'heigh'])
Weather = namedtuple('Weather', ['current', 'feels_like', 'max', 'min', 'description', 'icon'])

def build_payload(search, **params):
    payload = {
        'q': search,
        'cx': os.getenv('SEARCH_ID'),
        'key': os.getenv('API_KEY'),
        'imgType': 'photo',
        'searchType': 'image',
    }
    payload.update(params)
    return payload


def fetch_image(search, imgSize='xxlarge', imgDominantColor='blue'):
    url = 'https://customsearch.googleapis.com/customsearch/v1'

    params = build_payload(search, imgSize=imgSize, imgDominantColor=imgDominantColor)
    try:
        response = requests.get(url, params=params)
    except:
        raise

    Image = namedtuple('Image', ['link', 'width', 'heigh'])
    try:
        items = response.json()['items']
        images = [Image(
            link=item.get('link', ''),
            width=item['image'].get('width'),
            heigh=item['image'].get('height'))
                  for item
                  in items]

        images = [image for image in images if image.width > image.heigh]
        return images[0].link
    except:
        raise


def fetch_weather(city, units):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': os.getenv('WEATHER_API'),
        'units': units,
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
    except:
        raise


    weather = Weather(
        current=data['main']['temp'],
        feels_like=data['main']['feels_like'],
        max=data['main']['temp_max'],
        min=data['main']['temp_min'],
        description=data['weather'][0]['description'],
        icon=data['weather'][0]['icon'],
    )

    return weather

if __name__ == '__main__':
    # fetch_image('cloudy+sky+1920x1080', imgDominantColor='black')
    fetch_weather('sopron', 'metric')