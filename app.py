from flask import Flask, request, render_template
from Class.ultramsg import Ultramsg
from Class.aami import AsteriskAmi
from models.handle_call import Attempts, Cdr, CallerStat, CalledStat, UniqueLink

app = Flask(__name__)


# DEFINITION DES ROUTES
@app.post("/")
def make_call_from_whatsapp():
    bot = Ultramsg(request.json)
    phones = bot.Processingـincomingـmessages()
    if phones:
        ami = AsteriskAmi(phones["chatId"], phones["caller"], phones["receiver"])
        call = ami.make_external_call()
    return "make call"

@app.get("/")
def home():
    return "Home"

@app.get("/cdr")
def cdr():
    return "Cdr"

@app.get("/caller")
def caller_stat():
    return "Caller stat"

@app.get("/called")
def called_stat():
    return "Called stat"

@app.get("/link")
def unique_link():
    return "Unique link"

@app.get("/internal")
def make_an_internal_call():
    ami = AsteriskAmi("", "701", "702")
    call = ami.make_internal_call()
    print(call)
    return "e"


if (__name__) == "__main__":
    app.run()
