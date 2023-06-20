from flask import Flask, request, render_template
from Class.ultramsg import Ultramsg

app = Flask(__name__)


# DEFINITION DES ROUTES
@app.post("/")
def make_call_from_whatsapp():
    bot = Ultramsg(request.json)
    phones = bot.Processingـincomingـmessages()
    if phones:
        print(phones)


if (__name__) == "__main__":
    app.run()
