import logging

__logger = logging.getLogger("YT")
__logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(name)s] - %(message)s")
handler.setFormatter(formatter)
__logger.addHandler(handler)
