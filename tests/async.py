from threading import Thread
from utils import Logger
from random import choice
from faker import Faker
from time import sleep

logger = Logger(__name__)
fake = Faker('en_US')

LEVELS = ['info', 'error', 'warn', 'debug']
NUMBER = 10


def _write():
    for i in range(100):
        level = choice(LEVELS)
        content = fake.sentence(5)

        launch = getattr(logger, level)
        if launch:
            launch(content)

        sleep(.5)

for i in range(NUMBER):
    log = Thread(target=_write, args=[], daemon=True)
    log.start()