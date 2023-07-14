from flask import Flask, request, render_template, url_for
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
        
        ami = AsteriskAmi("", phones["caller"], phones["receiver"])
        call = ami.make_external_call()
        print(call)
            
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
                    called_stat.add(phones["receiver"], 0)
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
                    called_stat.add(phones["receiver"], 0)
                    called_stat.unanswered(phones["receiver"])
                else:
                    called_stat.unanswered(phones["receiver"])
    return "external call"

@app.get("/")
def home():
    attempt = Attempts()
    return render_template("index.html", attempts=attempt.get_all())

@app.get("/cdr")
def cdr():
    cdr = Cdr()
    return render_template("cdr.html", cdrs=cdr.get_all())

@app.get("/caller")
def caller_stat():
    caller_stat=CallerStat()
    return render_template("caller_stats.html", caller_stats=caller_stat.get_all())

@app.get("/called")
def called_stat():
    called_stat=CalledStat()
    return render_template("called_stats.html", called_stats=called_stat.get_all())

@app.get("/link")
def unique_link():
    unique_link=UniqueLink()
    return render_template("link.html", links=unique_link.get_all())

@app.post("/internal")
def make_an_internal_call():
    phones={"caller":"702", "receiver":"701"}
    attempt = Attempts()
    attempt.add(phones["caller"], phones["receiver"])
    
    ami = AsteriskAmi("", phones["caller"], phones["receiver"])
    call = ami.make_internal_call()
    print(call)
        
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
                called_stat.add(phones["receiver"], 0)
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
                called_stat.add(phones["receiver"], 0)
                called_stat.unanswered(phones["receiver"])
            else:
                called_stat.unanswered(phones["receiver"])
    return "internal call"


if (__name__) == "__main__":
    app.run()
