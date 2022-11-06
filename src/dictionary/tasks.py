from celery import shared_task
from celery.utils.log import get_task_logger
from dictionary.models import Word

from backend.celery import app

logger = get_task_logger(__name__)


@app.task
def add_word(word, value):
    """Register new word in the db.

    :param word: string, word name to be added
    :param value: string, word value describing the name
    :return: None
    """
    logger.info("adding new word")
    Word.objects.create(value=word, description=value)
