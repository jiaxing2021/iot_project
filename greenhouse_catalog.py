import cherrypy
import json

class catalog(object):
    exposed = True

    def GET(self, *uri):
        if len(uri) == 1:
            string = uri[0]
            if string == "token":
                with open('token.json') as file:
                        settings = json.load(file)
                result = settings["token"]
                return result
            
            if string == "broker":
                result = {"ec_settings":"","fcommand_setting":""}
                with open('ec_settings.json') as file:
                        settings = json.load(file)
                        result["ec_settings"] = settings
                with open('fcommand_setting.json') as file:
                        settings = json.load(file)
                        result["fcommand_setting"] = settings

                return json.dumps(result)
            
            if string == "chatID":
                with open('chatID.json') as file:
                        settings = json.load(file)
                result = settings["chatID"]
                result = result[-1]
                return result
            
            if string == "chatIDList":
                with open('chatID.json') as file:
                        settings = json.load(file)
                result = json.dumps(settings)
                return result
            
            if string == "temperature":
                with open('sensor_log.json') as file:
                    result = json.load(file)
                result = result['data'][0]['t'] 
                
                result = result[-5] + '  ' + result[-4] + '  ' + result[-3] + '  ' + result[-2] + '  ' + result[-1]
                return result
                
            if string == "humidity":
            
                with open('sensor_log.json') as file:
                    result = json.load(file)
                result = result['data'][1]['h'] 
                
                result = result[-5] + '  ' + result[-4] + '  ' + result[-3] + '  ' + result[-2] + '  ' + result[-1]
                return result
            
            if string == "predicted":
            
                with open('predicted_log.json') as file:
                    temp_result = json.load(file)
                temp_result = temp_result['data'][0]['t'] 
                
                temp_result = temp_result[-5] + '  ' + temp_result[-4] + '  ' + temp_result[-3] + '  ' + temp_result[-2] + '  ' + temp_result[-1]
            
                with open('predicted_log.json') as file:
                    humd_result = json.load(file)
                humd_result = humd_result['data'][1]['h'] 
                humd_result = humd_result[-5] + '  ' + humd_result[-4] + '  ' + humd_result[-3] + '  ' + humd_result[-2] + '  ' + humd_result[-1]
            
                return json.dumps({"temp_result":temp_result, "humd_result":humd_result})
        
                
            if string == "status_mechanism":
                    result = json.load(open('command_log.json'))
                    
                    return json.dumps(result)
        if len(uri) == 2:
             if uri[0] == 'newtoken':
                with open("token.json") as file:
                    dic = json.load(file)
                dic["token"] = uri[1]

                with open('token.json','w') as file:
                     json.dump(dic, file)
             return uri[1]
        
        
    # def POST(self, *uri):

    #     if len(uri)!=0:
    #         # output+=str(para)
    #         if uri[0] == 'newtoken':
    #             with open("token.json") as file:
    #                 dic = json.load(file)
    #             dic["token"] = uri[1]

    #             with open('token.json','w') as file:
    #                  json.dump(dic, file)
                     


if __name__ == "__main__":
    # Standard configuration to serve the url "localhost:8080"
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on': True
        }
    }
    webService = catalog()
    cherrypy.tree.mount(webService, '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
