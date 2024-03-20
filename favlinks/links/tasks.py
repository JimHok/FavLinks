from celery import shared_task
from celery.utils.log import get_task_logger
from time import sleep

logger = get_task_logger(__name__)


@shared_task
def get_links():
    for i in range(11):
        logger.info(i)
        sleep(1)
    return "Task completed!"
