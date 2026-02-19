LAB Project for Arduino/Raspberry PI for camper/van application

The hardware is going to be used on a camper/van
- as weather station with history, with the possibility to be consulted remotely, queried on an app for android/iphone, or via ssh
- as anti-thief system to track the van in case it gets stolen
- water tanks temperature and levels check
- tilt solar panels to get best electricity production

The scripts/functions will be manually managed/accessed via ssh, or via android/apple application

<br>
ROADMAP

Completed:
+ hardware (Arduino, Raspberry PI Zero 2W)
  soldering, configuring
+ temperature/humidity/pressure sensor BME280
  connecting
  sketch for arduino to read the values and send them out
+ implementing readings (bme_logger.py file to intercept the arduino outputs and store them to the database)
+ database to archive the readings and allow queries via sqlite3
+ creation of the service bme_logger.service, starting on boot, always restarting, to maintain the readngs active
+ creation of a script(bme_graph.py) to visually review on a graph (bme_graph.png) the data in a specific time frame chose by user
+ implement heartbeat check and reset of Arduino
+ Install Tailscale on RaspberryPI, to allow remote access


Next:

- hardware:
    - add and configure gsm/5g or hotspot access
- implement android/iphone application to connect and interact with Raspberry
- hardware
    - frame and motor to tilt solar panels
    - gps on raspberry
- implement the script to tilt or close the solar panels based on
    - latitude
    - time of the day
    - time of the year
    - orientation N/S
- hardware
  - voltage sensor
- implement script for reading the voltage from the battery
- hardware
  - waterproof temperature sensors for water tanks
- implement reading of the sensors
  - adding the data to the database
- hardware
  - tanks level sensors
- implement script for reading waer level sensosrs
-  implement script for alerts
  - anti-thief (movement when it is supposed to be parked, sending location)
  - water tank temperature (when the temperature is too low for too long)
  - water level (time to refill or drain)
- implement the android/apple application to include the new features when added
- possibility to configure the application with all the features or only with some of them, based on the hardware availability 
