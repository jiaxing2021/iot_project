# iot_project
## mosquitto.conf is for Message brocker
## GreenHouse_catalog.py is for GreenHouse Catalog
## raspberry.py is for Raspberry Pi Connector, whose function are that publishing data from sensors and subscripting the command from Post Process part through Message brocker.
## environment_control.py and post_statistics.py are for Post Process part, whose functions are subscripting data and publishing commands with Raspberry Pi Connect part.
## TS_adapter.py is for Thingspeak adapter.

# run the codes
## first run raspberry.py
## and then run environment_control.py and post_statistics.py
## for Thingspeak and freeboard part, you need to creat accounts and change the code in TS_adapter.py
## for telegram bot run the code telebot.py and don't forget to change token
