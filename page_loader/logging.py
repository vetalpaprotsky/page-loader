import logging
import logging.config
import sys

logging.basicConfig(
    format=('%(asctime)s - %(levelname)s - '
            '%(filename)s:%(lineno)d - %(message)s'),
    level=logging.INFO,
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)
