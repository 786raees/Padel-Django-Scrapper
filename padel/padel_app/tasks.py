import subprocess
from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task
def run_scrapper():
    logger.info("\nstarting matchi scrapper.\n")
    subprocess.run(['scrapy', 'crawl', 'matchi'])
    # logger.info("\nstarting matchi playtomic.\n")
    # subprocess.run(['scrapy', 'crawl', 'playtomic'])
