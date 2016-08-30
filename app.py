from RegistrarSpider import RegistrarSpider
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from multiprocessing.queues import Queue
from multiprocessing import Process
from flask import Flask, url_for
import os, signal

class CrawlerWorker(Process):
    def __init__(self, spider, result):
        Process.__init__(self)

        self.crawler = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        self.spider = spider
        self.result = result

    def run(self):
        self.crawler.crawl(self.spider, result=self.result)
        self.crawler.start()
        self.crawler.stop()
        print "!!!PID:", os.getppid()


app = Flask(__name__)

#app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

@app.route("/")
def index():
    return "test"

@app.route("/refresh")
def refresh():
    result = Queue()
    crawler = CrawlerWorker(RegistrarSpider, result)
    crawler.start()
    tmp = result.get()
    crawler.join()
    crawler.terminate()
    return tmp.encode('utf8')


if __name__ == "__main__":
    app.run()
