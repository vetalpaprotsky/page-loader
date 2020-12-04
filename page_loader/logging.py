import logging
import sys

logger = logging.getLogger('page-loader')
logger.setLevel(logging.DEBUG)
_handler = logging.StreamHandler(sys.stderr)
_handler.setLevel(logging.WARNING)
_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
_handler.setFormatter(_formatter)
logger.addHandler(_handler)
