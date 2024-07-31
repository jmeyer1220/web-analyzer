from flask import Blueprint, jsonify, request
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import whatcms
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

main = Blueprint('main', __name__)

@main.route('/analyze', methods=['POST'])
def analyze():
    url = request.json['url']

