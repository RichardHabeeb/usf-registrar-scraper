from flask import Flask, send_from_directory, render_template
import subprocess, time, threading, signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

app = Flask(__name__, static_url_path='')
#app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

CACHE_SECONDS = 60*30

current_fetch_data = ""
next_fetch_data = ""

@app.route("/")
@app.route("/current")
def current():
    return render_template('index.html', text='c')

@app.route("/next")
def next():
    return render_template('index.html', text='n')

@app.route("/c")
def currenttable():
    return current_fetch_data

@app.route("/n")
def nexttable():
    return next_fetch_data #We cannot send this data with the template because it isn't sanitized for the Jinja2 compiler.

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('fonts', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)


def refresh_cache():
    global next_fetch_data, current_fetch_data
    next_fetch_data = subprocess.Popen(["scrapy", "runspider", "NextSemesterSpider.py"], stdout=subprocess.PIPE).communicate()[0]
    current_fetch_data = subprocess.Popen(["scrapy", "runspider", "CurrentSemesterSpider.py"], stdout=subprocess.PIPE).communicate()[0]
    threading.Timer(CACHE_SECONDS, refresh_cache).start()

refresh_cache()

if __name__ == "__main__":
    app.run()
