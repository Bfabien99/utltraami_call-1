import json
import requests
import json
from keys import ULTRAMSG_CREDENTIALS

class Ultramsg:
    def __init__(self, json):
        self.json = json
        self.dict_messages = json["data"]
        self.__ultraAPIUrl = f"https://api.ultramsg.com/"+{ULTRAMSG_CREDENTIALS.get("instance")}+"/"
        self.__token = {ULTRAMSG_CREDENTIALS.get("token")}
    
    # ENVOYER DES REQUETES A L'API
    def send_requests(self, type, data={}):
        url = f"{self.__ultraAPIUrl}{type}?token={self.__token}"
        headers = {"Content-type": "application/json"}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()
    
    # ENVOYER UN MESSAGE SUR WHATSAPP
    def send_message(self, chatID, text):
        data = {"to": chatID, "body": text}
        answer = self.send_requests("messages/chat", data)
        return answer

    # REPONSE AUTOMATIQUE
    def welcome(self, chatID):
        welcome_string = "Pour passer un appel, vous pouvez directement composer le numéro du correspondant en respectant ce format : _225XXXXXXXXXX_\n"
        welcome_string += "*_Exemple_: 2250101020102*"
        return self.send_message(chatID, welcome_string)
    
    # LA LOGIQUE DU PROGRAMME
    def Processingـincomingـmessages(self):
        if self.dict_messages != []:
            message = self.dict_messages
            print("dict_message : ", self.dict_messages)
            print(message)