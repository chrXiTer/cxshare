from scrapy.cmdline import execute
from proj.spiders import hyx_js0
import sys
import os

def pqsj(scrapyName, id):
    hyx_js0.allIds=[id]
    execute(['scrapy','crawl', scrapyName , '-o', 'books.csv']) # 启动爬虫,第三个参数为爬虫name