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
        attempt = Attempts()
        attempt.add(phones["caller"], phones["receiver"])
        ami = AsteriskAmi(phones["chatId"], phones["caller"], phones["receiver"])
        call = ami.make_external_call()
        
        if call:
            caller_stat = CallerStat()
            called_stat = CalledStat()
            
            unique_link = UniqueLink()
            unique_link.add(phones["caller"], phones["receiver"])
            
            if call.get("cdr") != {}:
                cdr = Cdr()
                cdr.add(phones["caller"], phones["receiver"], call['cdr']['StartTime'], call['cdr']['AnswerTime'], call['cdr']['EndTime'], call['cdr']['Duration'], call['cdr']['BillableSeconds'], call['cdr']['Disposition'], call['cdr']['UniqueID'])
                
            if call.get('bridge') != {}:
                if not caller_stat.exist(phones["caller"]):
                    caller_stat.add(phones["caller"])
                    caller_stat.answered(phones["caller"])
                else:
                    caller_stat.answered(phones["caller"])
                    
                if not called_stat.exist(phones["receiver"]):
                    called_stat.add(phones["receiver"])
                    called_stat.answered(phones["receiver"])
                else:
                    called_stat.answered(phones["receiver"])
            else:
                if not caller_stat.exist(phones["caller"]):
                    caller_stat.add(phones["caller"])
                    caller_stat.unanswered(phones["caller"])
                else:
                    caller_stat.unanswered(phones["caller"])
                    
                if not called_stat.exist(phones["receiver"]):
                    called_stat.add(phones["receiver"])
                    called_stat.unanswered(phones["receiver"])
                else:
                    called_stat.unanswered(phones["receiver"])
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
