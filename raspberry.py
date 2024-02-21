from MyMQTT import *
import time
import json
import random
import cherrypy
import pandas as pd
import RPi.GPIO as GPIO

heating = 11
watering = 13
fertilizer = 15
GPIO.setmode(GPIO.BOARD)
GPIO.setup(heating, GPIO.OUT)
GPIO.setup(watering, GPIO.OUT)
GPIO.setup(fertilizer, GPIO.OUT)

class ec_pub:
	def __init__(self, clientID, topic,broker,port):
		self.topic=topic
		self.client=MyMQTT(clientID,broker,port,None)
		
	def start (self):
		self.client.start()

	def stop (self):
		self.client.stop()

	def publish(self,temp,humid):
		try:
			with open('sensor_log.json') as file:
				data = json.load(file)

			data['data'][0]['t'].append(eval(temp))
			data['data'][1]['h'].append(eval(humid))
			
			with open('sensor_log.json','w') as file:
				json.dump(data, file)
		except:
			data = {'data':[{'t':[]},{'h':[]}]}
			data['data'][0]['t'].append(eval(temp))
			data['data'][1]['h'].append(eval(humid))
			

			with open('sensor_log.json','w') as file:
				json.dump(data, file)


			
		message = {'data':[{'t':''},{'h':''}]}
		message['data'][0]['t']=str(temp)
		message['data'][1]['h']=str(humid)
		self.client.myPublish(self.topic,message)
		with open('sensor_log.json', 'w') as file:
			json.dump(data, file)
		print("ec data published and saved")
		
		time.sleep(1)

class TS_pub(ec_pub):
	def publish(self,temp,humid):

		message = {'data':[{'t':''},{'h':''}]}
		message['data'][0]['t']=str(temp)
		message['data'][1]['h']=str(humid)
		self.client.myPublish(self.topic,message)
		print("TS data published")
		
		time.sleep(1)
	

class ec_com_sub:
	def __init__(self, clientID, topic, broker, port):
		self.client = MyMQTT(clientID, broker, port, self)
		self.topic = topic
		self.status = None

	def start(self):
		self.client.start()
		self.client.mySubscribe(self.topic)

	def stop(self):
		self.client.stop()

	def notify(self, topic, msg):
		d = json.loads(msg)
		# print(type(d))
		print(d[0])
		
		if d[0] == 'heating':
			if d[1] == 'on':
				GPIO.output(heating, GPIO.HIGH)
				print('bot_on')
			if d[1] == 'off':
				GPIO.output(heating, GPIO.LOW)
		elif d[0] == 'watering':
			if d[1] == 'on':
				GPIO.output(watering, GPIO.HIGH)
			if d[1] == 'off':
				GPIO.output(watering, GPIO.LOW)
		elif d[0] == 'fer':
			if d[1] == 'on':
				GPIO.output(fertilizer, GPIO.HIGH)
				time.sleep(5)
				GPIO.output(fertilizer, GPIO.LOW)
		else:
			with open('command_log.json') as self.file:
				self.data = json.load(self.file)
			
			self.data['data'][0]['Heating'] = d[0]
			self.data['data'][1]['Watering'] = d[1]
			
			with open('command_log.json', 'w') as self.file:
				json.dump(self.data, self.file)

			'''
			code for raspberry GPIO control
			'''
			if self.data['data'][0]['Heating'] == 'on':
				GPIO.output(heating, GPIO.HIGH)
			if self.data['data'][0]['Heating'] == 'off':
				GPIO.output(heating, GPIO.LOW)

			if self.data['data'][1]['Watering'] == 'on':
				GPIO.output(watering, GPIO.HIGH)
			if self.data['data'][1]['Watering'] == 'off':
				GPIO.output(watering, GPIO.LOW)

		print("ec com sub done")

class fer_com_sub:
	def __init__(self, clientID, topic, broker, port):
		self.client = MyMQTT(clientID, broker, port, self)
		self.topic = topic
		self.status = None

	def start(self):
		self.client.start()
		self.client.mySubscribe(self.topic)

	def stop(self):
		self.client.stop()

	def notify(self, topic, msg):
		d = json.loads(msg)
		print(d)
		if d == "fer_on":
			GPIO.output(fertilizer, GPIO.HIGH)

			time.sleep(3)
			GPIO.output(fertilizer, GPIO.LOW)
		
		try:
			with open('fer_command_log.json') as self.file:
				self.data = json.load(self.file)
			self.data['fertilizer'] = d
			
		except:
			self.data = {}
			self.data['fertilizer'] = d
			with open('fer_command_log.json', 'w') as self.file:
				json.dump(self.data, self.file)

		

		print("fertilizer done")

	
if __name__ == "__main__":

	data = pd.read_csv("./data.csv")

	temp = data['temp'].tolist()
	humidity = data['humidity'].tolist()

	print("=================sub=================")

	conf = json.load(open("command_setting.json"))
	broker = conf["broker"]
	port = conf["port"]
	topic = conf['baseTopic']
	ec_sub = ec_com_sub("ec_com_sub", topic, broker, port)

	conf_fer = json.load(open("fer_command_setting.json"))
	broker_fer = conf_fer["broker"]
	port_fer = conf_fer["port"]
	topic_fer = conf_fer['baseTopic']
	fer_sub = fer_com_sub("fer_com_sub", topic_fer, broker_fer, port_fer)

	ec_sub.start()
	fer_sub.start()
	# bot_sub.start()

	print("=================pub=================")
	conf=json.load(open("ec_settings.json"))
	broker=conf["broker"]
	port=conf["port"]
	topic = conf['baseTopic']
	ec_pub = ec_pub("ec_pub",topic,broker,port)
	ec_pub.client.start()

	conf_TS=json.load(open("post_ec_setting.json"))
	broker_TS=conf_TS["broker"]
	port_TS=conf_TS["port"]
	topic_TS = conf_TS['baseTopic']
	TS_pub = TS_pub("TS_pub",topic_TS,broker_TS,port_TS)
	TS_pub.client.start()

	time.sleep(2)

	sleeptime = 5
	t = sleeptime

	i = 0
	while True:
		if i < len(temp):
			with open('sensor_setting.json') as file:
				dic = json.load(file)
				temp_num = dic["sensor_num"][0]['temp']
				humidity_num = dic["sensor_num"][1]['humidity']
				temp_input = []
				humid_input = []
				for j in range(temp_num):
					temp_input.append(temp[i] + random.random())
				temp_input = sum(temp_input)/temp_num
				temp_input = format(temp_input, '.2f')
				temp_input = str(temp_input)
				for j in range(humidity_num):
					humid_input.append(humidity[i] + random.random())
				humid_input = sum(humid_input)/humidity_num
				humid_input = format(humid_input, '.2f')
				humid_input = str(humid_input)
				ec_pub.publish(temp_input, humid_input)
				TS_pub.publish(temp_input, humid_input)
			i += 1
			time.sleep(t)
		else:
			i = 0
		
	cherrypy.engine.block()
	ledManager.client.stop()   