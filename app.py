from flask import Flask, request, jsonify
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import whatcms
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

class WebsiteSpider(scrapy.Spider):
    name = 'website_spider'
    
    def __init__(self, start_url=None, *args, **kwargs):
        super(WebsiteSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).netloc]
        self.pages = []

    def parse(self, response):
        self.pages.append(response.url)
        # Implement page parsing and categorization logic here
        for href in response.css('a::attr(href)'):
            yield response.follow(href, self.parse)

def crawl_website(url):
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    })
    spider = WebsiteSpider(start_url=url)
    process.crawl(spider)
    process.start()
    return spider.pages

def detect_cms(url):
    result = whatcms.identify_cms(url)
    return result.get('name', 'Unknown')

def get_performance_metrics(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    # Implement performance metric collection here
    driver.quit()
    return {"load_time": "2.5s"}  # Placeholder
@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.json['url']
    
    pages = crawl_website(url)
    cms = detect_cms(url)
    performance_metrics = get_performance_metrics(url)
    
    return jsonify({
        "total_pages": len(pages),
        "cms": cms,
        "performance_metrics": performance_metrics
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)