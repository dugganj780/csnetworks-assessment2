#!/usr/bin/python3

import requests
from sense_hat import SenseHat
from urllib.request import urlopen
import  json
import  time

sense = SenseHat()

URL = 'https://prodapi.metweb.ie/weather/short/Cork'

r = requests.get(url = URL)

data = r.json()

temperature = float(data['temperature'])
windSpeed = float(data['windSpeed'])
rainfall = float(data['rainfall'])

print("Temperature: "+ str(temperature))
print("Rainfall: "+ str(rainfall))
print("Wind Speed: "+ str(windSpeed))

for x in range(0,8):
  for y in range(0,4):
    if rainfall <= 1:
      sense.set_pixel(x, y, 0, 255, 0)
    elif rainfall > 1 and rainfall <= 2:
      sense.set_pixel(x, y, 125, 125, 0)
    else:
      sense.set_pixel(x, y, 255, 0, 0)

for x in range(0,4):
  for y in range(4,8):
    if temperature >= 12:
      sense.set_pixel(x, y, 0, 255, 0)
    elif temperature < 12 and temperature >= 5:
      sense.set_pixel(x, y, 125, 125, 0)
    else:
      sense.set_pixel(x, y, 255, 0, 0)

for x in range(4,8):
  for y in range(4,8):
    if windSpeed <= 12:
      sense.set_pixel(x, y, 0, 255, 0)
    elif windSpeed > 12 and windSpeed <= 38:
      sense.set_pixel(x, y, 125, 125, 0)
    else:
      sense.set_pixel(x, y, 255, 0, 0)

ans = 0
WRITE_API_KEY='1QPWG43Z81FGK5R8'

baseURL='https://api.thingspeak.com/update?api_key=%s' % WRITE_API_KEY


while True:
  for event in sense.stick.get_events():
    if event.action == "pressed":
      if event.direction == "up":
        ans = 1
        conn = urlopen(baseURL + '&field1=%s' % (ans) + '&field2=%s' % (rainfall) + '&field3=%s' % (temperature) + '&field4=%s' % (windSpeed))
        print(conn.read())
        conn.close()
        sense.clear()
      elif event.direction == "down":
        ans = 0
        conn = urlopen(baseURL + '&field1=%s' % (ans) + '&field2=%s' % (rainfall) + '&field3=%s' % (temperature) + '&field4=%s' % (windSpeed))
        print(conn.read())
        conn.close()
        sense.clear()
      else:
        sense.clear()
