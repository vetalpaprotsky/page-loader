import requests
from page_loader.logging import logger


def get_content(url, decode=False):
    REQUEST_TIMEOUT = 10

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        if response.encoding is None:
            response.encoding = 'utf-8'

        logger.info(f'Got successful response from {url}')
        return response.text if decode else response.content
    except requests.exceptions.RequestException:
        logger.error(f'Got unsuccessful response from {url}')
        raise
