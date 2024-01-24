from MyMQTT import *
import time
import json
import random
import cherrypy
import pandas as pd

class ec_pub:
	def __init__(self, clientID, topic,broker,port):
		self.topic=topic
		self.client=MyMQTT(clientID,broker,port,None)
		
	def start (self):
		self.client.start()

	def stop (self):
		self.client.stop()

	def publish(self,temp,humid):

		with open('sensor_log.json') as file:
			data = json.load(file)

		data['data'][0]['t'].append(temp)
		data['data'][1]['h'].append(humid)
		
		message = {'data':[{'t':''},{'h':''}]}
		message['data'][0]['t']=str(temp)
		message['data'][1]['h']=str(humid)
		self.client.myPublish(self.topic,message)
		with open('sensor_log.json', 'w') as file:
			json.dump(data, file)
		print("published and saved")
		
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
		with open('command_log.json') as self.file:
			self.data = json.load(self.file)

		self.data['data'][0]['Heating'] = d[0]
		self.data['data'][1]['Watering'] = d[1]
		with open('command_log.json', 'w') as self.file:
			json.dump(self.data, self.file)

		'''
		code for raspberry GPIO control
		'''

		print("done")

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
		# print(type(d))
		
		try:
			with open('fer_command_log.json') as self.file:
				self.data = json.load(self.file)
			self.data['fertilizer'] = d[0]
			
		except:
			data = {}
			data['fertilizer'] = d[0]
			with open('fer_command_log.json', 'w') as self.file:
				json.dump(data, self.file)

		'''
		code for raspberry GPIO control
		'''

		print("fertilizer done")

# class temp_humd(object):
# 	exposed = True
# 	def GET(self, *url):
# 		with open('sensor_log.json') as file:
# 			data = json.load(file)
		
# 		if len(url)!=0:
# 			if url[0] == "retrivetemphumd":
# 				return json.dumps(data)
	
if __name__ == "__main__":
	# print("=================REST=================")
	# conf={
    #     '/':{
    #         'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
    #         'tool.session.on':True
    #     }
    # }

	# webService=temp_humd()
	# cherrypy.tree.mount(webService,'/',conf)
	# # cherrypy.config.update({'server.socket_host': '127.0.0.100'})
	# # cherrypy.config.update({'server.socket_port': 8080})
	# cherrypy.engine.start()
	# # cherrypy.engine.block()

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

	print("=================pub=================")
	conf=json.load(open("ec_settings.json"))
	broker=conf["broker"]
	port=conf["port"]
	topic = conf['baseTopic']
	ec_pub = ec_pub("ec_pub",topic,broker,port)
	ec_pub.client.start()
	time.sleep(2)

	# t = 1*60*10 # second
	t = 2
	i = 0
	while True:
		if i < len(temp):

			temp_input = temp[i] + random.random()
			temp_input = format(temp_input, '.2f')
			temp_input = str(temp_input)
			humid_input = humidity[i] + random.random()
			humid_input = format(humid_input, '.2f')
			humid_input = str(humid_input)

			i += 1
			
			ec_pub.publish(temp_input, humid_input)
			
			time.sleep(t)
		else:
			i = 0
		
	cherrypy.engine.block()
	ledManager.client.stop()   