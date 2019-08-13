from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot Connected"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()

#taken from https://www.codementor.io/garethdwyer/building-a-discord-bot-with-python-and-repl-it-miblcwejz