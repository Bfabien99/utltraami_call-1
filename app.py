from flask import Flask, request, render_template
from Class.ultramsg import Ultramsg
from Class.aami import AsteriskAmi

app = Flask(__name__)

# DEFINITION DES ROUTES
@app.post("/")
def make_call_from_whatsapp():
    bot = Ultramsg(request.json)
    phones = bot.Processingـincomingـmessages()
    if phones:
        ami = AsteriskAmi(phones["chatId"], phones["caller"], phones["receiver"])
        data = ami.make_external_call()
    return "make call"

@app.get("/internal")
def make_an_internal_call():
    ami = AsteriskAmi("", "701", "702")
    data = ami.make_internal_call()
    #atempt = Attempts()
    #atempt.add("701", "702", "e")
    """
    'hangup': {'Event': 'Hangup', 'Privilege': 'call,all', 'Channel': 'PJSIP/701-0000005d', 'ChannelState': '5', 'ChannelStateDesc': 'Ringing', 'CallerIDNum': '701', 'CallerIDName': 'caller', 'ConnectedLineNum': '<unknown>', 'ConnectedLineName': '<unknown>', 'Language': 'en', 'AccountCode': '', 'Context': 'from-internal', 'Exten': 's', 'Priority': '1', 'Uniqueid': '1687265672.140', 'Linkedid': '1687265672.140', 'Cause': '17', 'Cause-txt': 'User busy'}
    """
    
   # atempt.add("701", "702", data["hangup"]['ChannelStateDesc'])
    return "e"

if (__name__) == "__main__":
    app.run()
