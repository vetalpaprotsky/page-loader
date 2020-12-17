import logging
import sys


def setup():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        stream=sys.stderr,
        level=logging.WARNING,
    )
