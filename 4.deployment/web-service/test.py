import requests


ride = {
'temp': 300, 
'rain_1h': 30,
'snow_1h': 1,
'clouds_all': 0
,'Rush Hour': 1,
'weather_Clear': 1,
'weather_Clouds': 1,
'weather_Drizzle': 0, 
'weather_Fog': 1,
'weather_Haze': 1, 
'weather_Mist': 0,
'weather_Rain': 1,
'weather_Smoke': 0,
'weather_Snow': 1,
'weather_Squall': 1,
'weather_Thunderstorm':0 
}

url = 'http://127.0.0.1:9696/predict'

response = requests.post(url, json=ride)
print(response.json())


