"""
Repl.It forever online patch
"""

import logging
import sys
import os

from flask import Flask
from threading import Thread

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask('Bot online page')

log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)

def set_home_page():
    global page

    link_to_bot = "https://vk.com/{screen_name}".format(
        screen_name = os.environ.get("MARCEL_BOT_SCREEN_NAME")
    )

    form = """
        <form action="{link_to_bot}">
            <button type="submit">
                Open
            </button>
        </form>
    """.format(
        link_to_bot = link_to_bot
    )

    page = """
        <center>
            <h1>
                Bot is polling at @{screen_name}
            </h1>
            {form}
        </center>
    """.format(
        screen_name = os.environ.get("MARCEL_BOT_SCREEN_NAME"),
        form = form,
    )

@app.route('/')
def home():
    return page

def keep_alive(debug):
    if debug:
        return
    
    set_home_page()

    def run():
        app.run(host='0.0.0.0', port=8080, use_evalex=(not debug))
        
    t = Thread(target=run)
    t.start()