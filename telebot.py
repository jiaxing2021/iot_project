import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json
import time
import cherrypy

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
            payload = self.__message.copy()
            payload["alert"] = time.time()
            payload["heatingAction"] = "on"
            self.bot.sendMessage(chat_ID, text="Heating switched on")

            self.data['data'][0]['Heating'] = "On"
            if self.watering == 'On':
                self.data['data'][1]['Watering'] = 'On'
            else:
                self.data['data'][1]['Watering'] = 'Off'

            with open('command_log.json', 'w') as file:
                json.dump(self.data, file)
        
        elif message == "/offheating":
            payload = self.__message.copy()
            payload["alert"] = time.time()
            payload["heatingAction"] = "off"
            self.bot.sendMessage(chat_ID, text="Heating switched off")

            self.data['data'][0]['Heating'] = "Off"
            if self.watering == 'On':
                self.data['data'][1]['Watering'] = 'On'
            else:
                self.data['data'][1]['Watering'] = 'Off'

            with open('command_log.json', 'w') as file:
                json.dump(self.data, file)

        elif message == "/onwatering":
            payload = self.__message.copy()
            payload["alert"] = time.time()
            payload["wateringAction"] = "on"
            self.bot.sendMessage(chat_ID, text="Watering switched on")

            if self.heating == 'On':
                self.data['data'][0]['Heating'] = 'On'
            else:
                self.data['data'][0]['Heating'] = 'Off'
            self.data['data'][1]['Watering'] = "On"

            with open('command_log.json', 'w') as file:
                json.dump(self.data, file)

        elif message == "/offwatering":
            payload = self.__message.copy()
            payload["alert"] = time.time()
            payload["wateringAction"] = "off"
            self.bot.sendMessage(chat_ID, text="Watering switched off")

            if self.heating == 'On':
                self.data['data'][0]['Heating'] = 'On'
            else:
                self.data['data'][0]['Heating'] = 'Off'
            self.data['data'][1]['Watering'] = "Off"

            with open('command_log.json','w') as file:
                json.dump(self.data, file)

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
            
            text = "Temperature is "+temp+"and humidity is "+humd+" And the predicted temperature is"+pre_temp+' the predicted humidity is '+pre_humd

            self.bot.sendMessage(chat_ID, text=text)

        elif message=="/onfer":
            try:
                with open('fer_flag.json') as file:
                    dic = json.load(file)
                dic['fer'] = 1
                with open('fer_flag.json','w') as file:
                    json.dump(dic, file)
            except:
                dic = {}
                dic['fer'] = 1
                with open('fer_flag.json','w') as file:
                    json.dump(dic, file)

        
            
            text = "fer on"
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
