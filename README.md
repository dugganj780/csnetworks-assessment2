# Computer Networks and Systems - Assessment 2
## James Duggan - 06357628

Welcome to my project. It is a simple app, written in Python, utilising a Raspberry Pi and various network connections to allow a user to see the status of the weather and use this information to decision make a decision on whther or not to drive to work that day.


### How to Use
1. Boot the RPi
2. The SenseHat LEDs should light up to represent the level of rainfall(top half), temperature(bottom left quarter), wind speed (bottom right quarter)
3. Weather Conditions are represented by colour: Green (good), Yellow (mild), and Red (poor)
4. If the user has a beacon scanner app on their phone, they can also use this to get a more accurate reading of the weather before making their choice
5. The user then makes their decision and inputs if they will be driving or not using the SenseHat: Up for Driving, Down for Walking
6. If the user selects to drive 3 days in a row or more, then they will receive and email reminding them to get some exercise

### How it Works
The Python Script runs on boot by including it in rc.local. This means the user will not need to ssh into the RPi using a laptop.
They do have the option to do this, however, and if they do they will see accurate readings of the weather and their selection.

Using  XML from Met Eireann website, current weather conditions are sent to the RPI and represented on the SenseHat LEDs.

The RPi also creates and Eddystone beacon that transmits an link to the Met Eireann website.
If the user has a beacon scanner app on their phone, they can use this to get a more accurate weather reading before making their decision.

ThingSpeak is used as IoT platform. RPI sends the user’s response and the weather conditions from Met Eireann to ThingSpeak and it keeps a record.
ThingSpeak also sends back the previous two responses from the user for calculation using an XML file. 
When the user has driven 3 times in a row, ThingSpeak sends them an email using IFTTT to remind them to exercise.
