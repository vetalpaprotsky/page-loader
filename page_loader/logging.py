import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
_handler = logging.StreamHandler(sys.stderr)
_handler.setLevel(logging.INFO)
_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
_handler.setFormatter(_formatter)
logger.addHandler(_handler)
