import logging

logging.basicConfig(filename='logs.log', level=logging.DEBUG,
    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="a")

logger = logging.getLogger(__name__)