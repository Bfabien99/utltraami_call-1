from pyami_asterisk import AMIClient

# PROPRE À MOI
from keys import AAMI_CREDENTIALS # contient nos clés d'identification
from Class.ultramsg import Ultramsg

class AsteriskAmi():
    def __init__(self, chatId:str="", caller:str="", receiver:str="") -> None:
        self.chatId=chatId
        self.caller_phone=caller
        self.receiver_phone=receiver
        
        self.__ami = AMIClient(host=AAMI_CREDENTIALS.get('host'), port=AAMI_CREDENTIALS.get('port'), username=AAMI_CREDENTIALS.get('username'), secret=AAMI_CREDENTIALS.get('secret'), reconnect_timeout=5)
        self.__ami.register_event(["*"], self.__cdr_callback)
        self.__ami.register_event(["*"], self.__hangup_callback)
        
    def make_external_call(self):
        try:
            self.__ami.register_event(["Originate"], self.__originateE_callback)
            self.__ami.create_action({
                "Action":"Originate",
                "Exten": f"{self.receiver_phone}",
                "Channel": f"PJSIP/{self.caller_phone}@serveur_externe_ci",
                "Context": "from-trunk",
                "Priority": "1",
                "CallerID": f"{self.caller_phone}",
            }, self.__originateE_callback)
            self.__ami.connect()
        except Exception as e:
            print("Error make_external_call:", e)
        
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
            
    def __cdr_callback(self, events):
        if events.get("Event") == "Cdr":
            print(events)
            
    def __hangup_callback(self, events):
        if events.get("Event") == "Hangup":
            print(events)
        
    def __originateI_callback(self, events):
        print("-- Internal originate call begin... --")
        print(events)
        
    def __originateE_callback(self, events):
        print("-- External originate call begin... --")
        print(events)
    
    def all_events(self, events):
        print(events)