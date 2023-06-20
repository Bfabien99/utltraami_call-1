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
        #ami = AsteriskAmi(phones["chatId"], phones["caller"], phones["receiver"])
        ami = AsteriskAmi(phones["chatId"], "701", "702")
        ami.make_internal_call()
        print(phones)
    return "make call"

@app.get("/internal")
def make_an_internal_call():
    ami = AsteriskAmi("", "701", "702")
    ami.make_internal_call()
    return "e"
if (__name__) == "__main__":
    app.run()
