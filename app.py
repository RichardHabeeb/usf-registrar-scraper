from flask import Flask, url_for
import subprocess

app = Flask(__name__)
#app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

@app.route("/")
def index():
    return "test"

@app.route("/refresh")
def refresh():
    output = subprocess.Popen(["scrapy", "runspider", "RegistrarSpider.py", "-s", "LOG_LEVEL=CRITICAL"], stdout=subprocess.PIPE).communicate()[0]
    return output

if __name__ == "__main__":
    app.run()
