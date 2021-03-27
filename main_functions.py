import asyncio
import json
from statistics import mean
import os
import requests


temperature_kharkov = []
openweather_api_key = os.environ.get('OPENWEATHER_API_KEY')
weatherstack_api_key = os.environ.get('WEATHERSTACK_API_KEY')


async def openweather_func():
    loop = asyncio.get_event_loop()

    request_openweather = loop.run_in_executor(None, requests.get,
                                               f'https://api.openweathermap.org/data/2.5/onecall?lat=49.9901&lon=36.2303&exclude=hourlys&appid=d{openweather_api_key}8&units=metric')

    openweather = await request_openweather

    json_openweather = json.loads(openweather.text)

    temperature_kharkov.append(json_openweather["daily"][0]["temp"]["morn"])


async def weatherstack_func():
    loop = asyncio.get_event_loop()

    request_weatherstack = loop.run_in_executor(None, requests.get,
                                                f'http://api.weatherstack.com/current?access_key={weatherstack_api_key}&query=Kharkiv')

    weatherstack = await request_weatherstack

    json_weatherstack = json.loads(weatherstack.text)

    temperature_kharkov.append(json_weatherstack['current']['temperature'])


async def metaweather_func():
    loop = asyncio.get_event_loop()

    request_metaweather = loop.run_in_executor(None, requests.get,
                                               'https://www.metaweather.com/api/location/922137/')

    metaweather = await request_metaweather

    json_metaweather = json.loads(metaweather.text)

    temperature_kharkov.append(json_metaweather["consolidated_weather"][0]["the_temp"])


loop = asyncio.get_event_loop()
loop.run_until_complete(openweather_func())
loop.run_until_complete(weatherstack_func())
loop.run_until_complete(metaweather_func())

avg_temperature_kharkov = mean(temperature_kharkov)

print("The temperature of the Kharkov =", round(avg_temperature_kharkov, 2), u'\u2103')
