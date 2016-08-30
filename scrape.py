#!/usr/bin/env python
import scrapy
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
import re
from flask import Flask
from multiprocessing import Process

app = Flask(__name__)

@app.route("/")
def hello():
    return "test"

class MySpider(scrapy.Spider):
    name = 'registrar'
    start_urls = ['http://www.registrar.usf.edu/ssearch/search.php']

    def parse(self, response):
        self.form = {}
        self.form[response.xpath("//tr[td='CAMPUS']/td/select/@name").extract()[0]] = "1"
        yield scrapy.FormRequest("http://www.registrar.usf.edu/ssearch/search.php",
                                   formdata=self.form,
                                   callback=self.campus_selected)

    def campus_selected(self, response):
        self.form[response.xpath("//tr[td='COLLEGE']/td/select/@name").extract()[0]] = "EN"
        yield scrapy.FormRequest("http://www.registrar.usf.edu/ssearch/search.php",
                                   formdata=self.form,
                                   callback=self.college_selected)

    def college_selected(self, response):
        self.form[response.xpath("//tr[td='DEPARTMENT']/td/select/@name").extract()[0]] = "ESB"
        yield scrapy.FormRequest("http://www.registrar.usf.edu/ssearch/search.php",
                                   formdata=self.form,
                                   callback=self.department_selected)

    def department_selected(self, response):
        self.form[response.xpath("//tr[td='TERM']/td/select/@name").extract()[0]] = "201608" # TODO COME BACK AND UPDATE THIS
        yield scrapy.FormRequest("http://www.registrar.usf.edu/ssearch/search.php",
                                   formdata=self.form,
                                   callback=self.term_selected)

    def term_selected(self, response):
        self.form[response.xpath("//tr[td='LEVEL']/td/select/@name").extract()[0]] = "GR"
        self.form[response.xpath("//tr[td='STATUS']/td/select/@name").extract()[0]] = ""
        self.form["search"] = "search"
        for name in response.xpath("//@name").extract():
            if 'P_' in name and name not in self.form:
                self.form[name] = ""

        yield scrapy.FormRequest("http://www.registrar.usf.edu/ssearch/search.php",
                                   formdata=self.form,
                                   callback=self.finished_search)

    def finished_search(self, response):
        num_resp = re.search(r"1 to [0-9]+ of ([0-9]+)", response.xpath("//div[@class='total']/span").extract()[0]).group(1)
        print "NUM RESPONSES:", num_resp
        yield scrapy.FormRequest("http://www.registrar.usf.edu/ssearch/results.php?P_RESULTS=" + num_resp,
                                   formdata=self.form,
                                   callback=self.full_results)

    def full_results(self, response):
        scraped_data = response.xpath("//table[@id='results']").extract()[0]


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(MySpider)
    process.start() # the script will block here until the crawling is finished
    process.stop()
    app.run()
