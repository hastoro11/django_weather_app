import requests
import os
from dotenv import load_dotenv
import asyncio
import aiohttp

load_dotenv('weather_project/.env')


def main(url):
    payload = build_payload('new+york', imgSize='xlarge', imgDominantColor='blue')
    r = requests.get(url,params=payload)
    try:
        items = r.json()['items']
        print(items[0]['link'])
    except Exception as err:
        print('Exception')
        print(err)

async def async_fetch(url):
    print('fetching url')
    payload = build_payload('tokyo', imgSize='xlarge', imgDominantColor='black')
    async with aiohttp.ClientSession() as session:
        r = await session.get(url=url, params=payload, ssl=False)

    print(r.status)
    print(await r.json())



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


if __name__ == '__main__':
    url = 'https://customsearch.googleapis.com/customsearch/v1'
    asyncio.run(async_fetch(url))

