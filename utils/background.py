"""
Костыль для repl.it
"""

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "I'm alive"


def keep_alive(debug):
  def run():
    app.run(host='0.0.0.0', port=8080, use_evalex=(not debug))
  t = Thread(target=run)
  t.start()