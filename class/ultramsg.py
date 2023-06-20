import json
import requests

# PROPRE À MOI
from keys import ULTRAMSG_CREDENTIALS # contient nos clés d'identification
from Class.parseNumber import ParseNumber

class Ultramsg:
    def __init__(self, json={}):
        self.json = json
        self.dict_messages = json.get("data")
        self.__ultraAPIUrl = f"https://api.ultramsg.com/{ULTRAMSG_CREDENTIALS.get('instance')}/"
        self.__token = ULTRAMSG_CREDENTIALS.get("token")
    
    # ENVOYER DES REQUETES A L'API
    def send_requests(self, type, data={}):
        url = f"{self.__ultraAPIUrl}{type}?token={self.__token}"
        headers = {"Content-type": "application/json"}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()
    
    # VERIFIER SI LE NUMERO EST WHATSAPP
    def is_whatsapp(self, phone_number_to_check):
        url = f"{self.__ultraAPIUrl}contacts/check?token={self.__token}&chatId={phone_number_to_check}"
        headers = {"Content-type": "application/json"}
        answer = requests.get(url, headers=headers)
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
        number_parser = ParseNumber()
        if self.dict_messages != []:
            #print("dict_message : ", self.dict_messages)
            """
            {'id': 'false_22504774183@c.us_3EB0717CB990A3FF06B0C4', 'from': '22504774183@c.us', 'to': '447458149047@c.us', 'author': '', 'pushname': 'Brou Kouadio Stéphane Fabien', 'ack': '', 'type': 'chat', 'body': 'Hello', 'media': '', 'fromMe': False, 'self': False, 'isForwarded': False, 'isMentioned': False, 'quotedMsg': {}, 'mentionedIds': [], 'time': 1687181008}
            
            * type : Le type de donnée reçu
                - chat : pour les messages text(emoji, textes)
                - ptt : pour le vocal
                - vcard : pour les contacts
                
            * from : L'expéditeur / correspond au chatID
            
            * to : Le recepteur
            
            * fromMe : si le message est envoyé par moi même
                - True/False
            """
            
            # S'ASSURER QUE LE MESSAGE NE VIENS PAS DE SOI MÊME
            if not self.dict_messages["fromMe"]:
                # ON VÉRIFIE QU'ON A REÇU DU TEXTE COMME MESSAGE
                if (self.dict_messages['type'] != "chat"):
                    self.send_message(self.dict_messages['from'], "❌ *Mauvaise entrée !*")
                    self.welcome(self.dict_messages['from'])
                    return False
                
                # ON RÉCUPÈRE LE MESSAGE ENVOYÉE PAR L'UTILISATEUR
                message_body = self.dict_messages["body"].split()
                message_recu = message_body[0]
                
                # VÉRIFIE QUE LE MESSAGE EST UN NUMÉRO ET QU'IL EST BIEN FORMATÉ/VALIDE
                if not number_parser.height_to_ten(message_recu):
                    self.send_message(self.dict_messages['from'], "❌ *Veuillez respecter le format requis !*")
                    self.welcome(self.dict_messages['from'])
                    return False
                
                # ON VÉRIFIE SI L'UTILISATEUR EST WHATSAPP
                if self.is_whatsapp(f"{number_parser.height_to_ten(message_recu)}@c.us").get("status") == 'valid':
                    # SI CET UTILISATEUR EST UN NUMERO WHATSAPP
                    numero_whatsapp=True
                else:
                    numero_whatsapp=False
                
                # ON RECUPÈRE LE NUMÉRO DE L'UTILISATEUR ET LE NUMÉRO À JOINDRE
                caller_phone = number_parser.whatsapp_to_civ(self.dict_messages['from'])
                receiver_phone = number_parser.height_to_ten(message_recu)
                
                # ON S'ASSURE QUE L'UTILISATEUR NE LANCE PAS D'APPEL VERS SON PROPRE NUMÉRO
                if caller_phone == receiver_phone:
                    self.send_message(self.dict_messages['from'], "❌ *Veuillez entrer un numéro différent du votre !*")
                    return False
                
                data = {"chatId":self.dict_messages['from'], "caller":caller_phone, "receiver":receiver_phone, "is_whatsapp":numero_whatsapp}
                return data
            
        else:
            print("no data")
            return False