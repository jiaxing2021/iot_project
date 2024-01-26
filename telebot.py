import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json
import time
import cherrypy
from MyMQTT import MyMQTT

class bot_com_pub:
    def __init__(self, clientID, topic,broker,port):
        self.topic=topic
        self.client=MyMQTT(clientID,broker,port,None)
        
    def start (self):
        self.client.start()

    def stop (self):
        self.client.stop()
    def publish(self,type,com):
        self.type = type
        self.com = com

        command = [self.type,self.com]
        self.client.myPublish(self.topic,command)
        time.sleep(1)

class RESTBot:
    exposed=True
    def __init__(self, token):
        # Local token
        self.tokenBot = token
        # Catalog token
        # self.tokenBot=requests.get("http://catalogIP/telegram_token").json()["telegramToken"]
        self.bot = telepot.Bot(self.tokenBot)
        self.chatIDs=[]
        self.__message={"alert":"","heatingAction":"","wateringAction":""}
        MessageLoop(self.bot, {'chat': self.on_chat_message}).run_as_thread()

        with open('command_log.json') as self.file:
            self.data = json.load(self.file)

        self.heating = self.data['data'][0]['Heating']
        self.watering = self.data['data'][1]['Watering']

    def on_chat_message(self, msg):
        content_type, chat_type, chat_ID = telepot.glance(msg)
        with open('chatID.json') as file:
            dic = json.load(file)
 
        with open('chatID.json', 'w') as file:
            dic["chatID"].append(str(chat_ID))
            json.dump(dic, file)

                    
        self.chatIDs.append(chat_ID)
        message = msg['text']
        if message == "/onheating":

            bot_pub.publish('heating','on')

            payload = self.__message.copy()
            payload["alert"] = time.time()
            payload["heatingAction"] = "on"
            self.bot.sendMessage(chat_ID, text="Heating switched on")

        
        elif message == "/offheating":

            bot_pub.publish('heating','off')

            payload = self.__message.copy()
            payload["alert"] = time.time()
            payload["heatingAction"] = "off"
            self.bot.sendMessage(chat_ID, text="Heating switched off")


        elif message == "/onwatering":

            bot_pub.publish('watering','on')

            payload = self.__message.copy()
            payload["alert"] = time.time()
            payload["wateringAction"] = "on"
            self.bot.sendMessage(chat_ID, text="Watering switched on")

        elif message == "/offwatering":

            bot_pub.publish('watering','off')

            payload = self.__message.copy()
            payload["alert"] = time.time()
            payload["wateringAction"] = "off"
            self.bot.sendMessage(chat_ID, text="Watering switched off")

        elif message == "/check":
            
            with open('command_log.json') as file:
                dic = json.load(file)
        
            heating_condition = dic['data'][0]['Heating']
            watering_condition = dic['data'][1]['Watering']

            
            text = "Heating is "+heating_condition+" and humidity is "+watering_condition

            self.bot.sendMessage(chat_ID, text=text)

        elif message=="/start":
            with open('sensor_log.json') as file:
                dic = json.load(file)
        
            temp = dic['data'][0]['t'][-1]
            humd = dic['data'][1]['h'][-1]

            with open('predicted_log.json') as file:
                data = json.load(file)

            pre_temp = data['data'][0]['t'][-1]
            pre_humd = data['data'][1]['h'][-1]
            
            text = "Temperature is "+str(temp)+" and humidity is "+str(humd)+" And the predicted temperature is"+str(pre_temp)+" the predicted humidity is "+str(pre_humd)

            self.bot.sendMessage(chat_ID, text=text)

        elif message=="/onfer":

            bot_pub.publish('fer','on')

            text = "fer on"
            self.bot.sendMessage(chat_ID, text=text)
        elif message=="/comlist":

            text = "/start /onheating /offheating /onwatering /offwatering /onfer /check /sensor_num"
            self.bot.sendMessage(chat_ID, text=text)
        elif message=="/sensor_num":
            
            with open('sensor_setting.json') as file:
                dic = json.load(file)
                temp_num = dic["sensor_num"][0]['temp']
                humidity_num = dic["sensor_num"][1]['humidity']

            
            text = "temp sensors number is "+str(temp_num)+" humidity sensors number is "+str(humidity_num)
            self.bot.sendMessage(chat_ID, text=text)

        else:
            self.bot.sendMessage(chat_ID, text="Command not supported")

    # def POST(self,*uri):
    #     tosend=''
    #     output={"status":"not-sent","message":tosend}
    #     if len(uri)!=0:
    #         if uri[0]=="led":
    #             body=cherrypy.request.body.read()
    #             jsonBody=json.loads(body)
    #             alert=jsonBody["alert"]
    #             action=jsonBody["action"]
    #             tosend=f"ATTENTION!!!\n{alert}, you should {action}"
    #             output={"status":"sent","message":tosend}
    #             for chat_ID in self.chatIDs:
    #                 self.bot.sendMessage(chat_ID, text=tosend)
    #         # for chat_ID in self.chatIDs:
    #         #     self.bot.sendMessage(chat_ID, text=tosend)
    #     return json.dumps(output)

if __name__ == "__main__":
    # conf = json.load(open("setting.json"))
    # token = conf["telegramToken"]
    conf = json.load(open("command_setting.json"))
    broker = conf["broker"]
    port = conf["port"]
    topic = conf['baseTopic']
    bot_pub = bot_com_pub("bot_com_pub", topic, broker, port)

    bot_pub.client.start()

    with open('token.json') as file:
        dic = json.load(file)
    token = dic["token"]
    # token = "6966081490:AAEJrzi2Ydu8RJO-uW0wzQwS_Y8XKbbBhLc"
    # token = "6503485157:AAGIhI08PpK5rZhkgLy3kwzK4PoZ4Jte4WE"
    cherryConf={
		'/':{
				'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
				'tool.session.on':True
		}
	}	
    bot=RESTBot(token)
    cherrypy.tree.mount(bot,'/',cherryConf)
    cherrypy.engine.start()
    cherrypy.engine.block()
