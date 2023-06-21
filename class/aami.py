from pyami_asterisk import AMIClient

# PROPRE À MOI
from keys import AAMI_CREDENTIALS # contient nos clés d'identification
from Class.ultramsg import Ultramsg
from datetime import datetime

class AsteriskAmi():
    def __init__(self, chatId:str="", caller:str="", receiver:str="") -> None:
        # AsteriskAmi self attributs
        self.chatId=chatId
        self.caller_phone=caller
        self.receiver_phone=receiver
        self.__data={"cdr":{}, "hangup":{}, "bridge":{}}
        
        # pyami_asterisk module initialistaion
        self.__ami = AMIClient(host=AAMI_CREDENTIALS.get('host'), port=AAMI_CREDENTIALS.get('port'), username=AAMI_CREDENTIALS.get('username'), secret=AAMI_CREDENTIALS.get('secret'), reconnect_timeout=5)
        self.__ami.register_event(["Cdr"], self.__cdr_callback)
        self.__ami.register_event(["Hangup"], self.__hangup_callback)
        self.__ami.register_event(["*"], self.__bridge_callback)
        
    def make_external_call(self):
        try:
            self.__ami.register_event(["Originate"], self.__originateE_callback)
            self.__ami.create_action({
                "Action":"Originate",
                "Exten": self.receiver_phone,
                "Channel": f"PJSIP/{self.caller_phone}@serveur_externe_ci",
                "Context": "from-trunk",
                "Priority": "1",
                "CallerID": f"{self.caller_phone}",
            }, self.__originateE_callback)
            self.__ami.connect()
        except Exception as e:
            print("Error make_external_call:", e)
        finally:
            return self.__data
        
    def make_internal_call(self): 
        try:
            self.__ami.register_event(["Originate"], self.__originateI_callback)
            self.__ami.create_action({
                "Action":"Originate",
                "Exten": self.receiver_phone,
                "Channel": f"PJSIP/{self.caller_phone}",
                "Context": "from-internal",
                "Priority": "1"
            }, self.__originateI_callback)
            self.__ami.connect()
        except Exception as e:
            print("Error make_internal_call:", e)
        finally:
            return self.__data
        
    async def __bridge_callback(self, events):
        if events.get("Event") == "BridgeEnter":
            self.__data["bridge"]=events
            
    def __cdr_callback(self, events):
        if events.get("Event") == "Cdr":
            self.__data["cdr"]=events
            
    async def __hangup_callback(self, events):
        if events.get("Event") == "Hangup":
            self.__data["hangup"]=events
            await self.__ami.connection_close()
        
    def __originateI_callback(self, events):
        print("-- Internal originate call begin... --")
        print(events)
        
    def __originateE_callback(self, events):
        print("-- External originate call begin... --")
        print(events)