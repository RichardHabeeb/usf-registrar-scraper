from flask import Flask, send_from_directory, render_template
import subprocess, datetime

app = Flask(__name__, static_url_path='')
#app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

CACHE_SECONDS = 60*30

current_fetch_time = None
current_fetch_data = ""
next_fetch_time = None
next_fetch_data = ""

@app.route("/")
def index():
    return render_template('index.html', text='currenttable')

@app.route("/current")
def current():
    return render_template('index.html', text='currenttable')

@app.route("/next")
def next():
    return render_template('index.html', text='nexttable')

@app.route("/currenttable")
def currenttable():
    global current_fetch_time, current_fetch_data
    now = datetime.datetime.now()
    if current_fetch_time is None or (now - current_fetch_time) > datetime.timedelta(seconds=CACHE_SECONDS):
        current_fetch_time = now
        current_fetch_data = subprocess.Popen(["scrapy", "runspider", "CurrentSemesterSpider.py"], stdout=subprocess.PIPE).communicate()[0]

    return current_fetch_data

@app.route("/nexttable")
def nexttable():
    global next_fetch_time, next_fetch_data
    now = datetime.datetime.now()
    if next_fetch_time is None or (now - next_fetch_time) > datetime.timedelta(seconds=CACHE_SECONDS):
        next_fetch_time = now
        next_fetch_data = subprocess.Popen(["scrapy", "runspider", "NextSemesterSpider.py"], stdout=subprocess.PIPE).communicate()[0]

    return next_fetch_data

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



if __name__ == "__main__":
    app.run()
