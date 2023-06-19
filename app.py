from flask import Flask, request, render_template
from Class.ultramsg import Ultramsg

app = Flask(__name__)

# DEFINITION DES ROUTES
@app.post("/")
def home_post():
    if request.method == "POST":
        bot = Ultramsg(request.json)
        bot.Processingـincomingـmessages()
    return "home"

if (__name__) == "__main__":
    app.run()