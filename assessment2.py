#!/usr/bin/python3

import requests
from sense_hat import SenseHat
from urllib.request import urlopen
import  json
import os
import sys

sense = SenseHat()

#Creating strings to access shell scripts using os later in the code
cmd1 = './eddy_start'
cmd2 = './beacon_stop'

#API from Met Eireann to get the current weather in Cork
URL = 'https://prodapi.metweb.ie/weather/short/Cork'

r = requests.get(url = URL)

data = r.json()

#Creating variables from the Met Eireann API
temperature = float(data['temperature'])
windSpeed = float(data['windSpeed'])
rainfall = float(data['rainfall'])

#Prints the variables to the console
print("Temperature: "+ str(temperature))
print("Rainfall: "+ str(rainfall))
print("Wind Speed: "+ str(windSpeed))

#API from ThingSpeak that is used to access the last 2 responses from the user
lastResponses = 'https://api.thingspeak.com/channels/1229784/fields/1.json?api_key=2AKCZ0ZYBBLVQPJM&results=2'

r2 = requests.get(url = lastResponses)

data2 = r2.json()

response1 = int(data2['feeds'][1]['field1'])
response2 = int(data2['feeds'][0]['field1'])

#Adding the responses gives how many times the user has driven so far
if response1 == 1:
  drove = response1 + response2
else:
  drove = 0

#Uses os to run the shell script that activates and Eddystone beacon that leads to the
#Met Eireann website, if the user needs to see an accurate reading of the weather 
os.system(cmd1)

#Creates and LED representation of the amount of rainfall on the SenseHat
#When the rain is less than 1mm the top half of the LEDs will be green, between 1 and 2mm
#it will be yellow, and over 2mm will be red
for x in range(0,8):
  for y in range(0,4):
    if rainfall <= 1:
      sense.set_pixel(x, y, 0, 255, 0)
    elif rainfall > 1 and rainfall <= 2:
      sense.set_pixel(x, y, 125, 125, 0)
    else:
      sense.set_pixel(x, y, 255, 0, 0)

#Creates and LED representation of the temperature on the SenseHat
#When the temperature is greater than 12C the bottom left quarter of the LEDs will be green, between 12 and 5C 
#it will be yellow, and under 5C will be red
for x in range(0,4):
  for y in range(4,8):
    if temperature >= 12:
      sense.set_pixel(x, y, 0, 255, 0)
    elif temperature < 12 and temperature >= 5:
      sense.set_pixel(x, y, 125, 125, 0)
    else:
      sense.set_pixel(x, y, 255, 0, 0)

#Creates and LED representation of the wind speed on the SenseHat
#When the windspeed is less than 12km/h the bottom right quarter of the LEDs will be green, between 12 and 38km/h
#it will be yellow, and over 38km/h will be red
for x in range(4,8):
  for y in range(4,8):
    if windSpeed <= 12:
      sense.set_pixel(x, y, 0, 255, 0)
    elif windSpeed > 12 and windSpeed <= 38:
      sense.set_pixel(x, y, 125, 125, 0)
    else:
      sense.set_pixel(x, y, 255, 0, 0)

#Declaring variable for the user's input with the joystick
ans = 0

#API url and key to send information back to ThingSpeak
WRITE_API_KEY='1QPWG43Z81FGK5R8'
baseURL='https://api.thingspeak.com/update?api_key=%s' % WRITE_API_KEY

#Loop to control user input using the joystick on the SenseHat 
while True:
  for event in sense.stick.get_events():
    if event.action == "pressed":
#When the user presses up, ans is set to one and added to the drove variable
#This is sent to ThingSpeak along with the weather stats
#The programme then closes and the SenseHat LEDs switch off
      if event.direction == "up":
        ans = 1
        last3ans = ans + drove
        print(last3ans)
        conn = urlopen(baseURL + '&field1=%s' % (ans) + '&field2=%s' % (rainfall) + '&field3=%s' % (temperature) + '&field4=%s' % (windSpeed) + '&field5=%s' % (last3ans))
        print(conn.read())
        conn.close()
        sense.clear()
        os.system(cmd2)
        sys.exit()

#When the user presses down, ans is set to zero multiplied by drove variable, resetting the last 3 responses from the user
#This is sent to ThingSpeak along with the weather stats
#The programme then closes and the SenseHat LEDs switch off
      elif event.direction == "down":
        ans = 0
        last3ans = ans * drove
        print(last3ans)
        conn = urlopen(baseURL + '&field1=%s' % (ans) + '&field2=%s' % (rainfall) + '&field3=%s' % (temperature) + '&field4=%s' % (windSpeed) + '&field5=%s' % (last3ans))
        print(conn.read())
        conn.close()
        sense.clear()
        os.system(cmd2)
        sys.exit()
      else:
        sense.clear()
        os.system(cmd2)
        sys.exit()
