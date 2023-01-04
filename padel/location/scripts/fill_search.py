from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run():
    process = CrawlerProcess(get_project_settings())
    process.crawl('search_list_spider')
    process.start() # the script will block here until the crawling is finished
