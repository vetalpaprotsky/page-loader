import requests
from page_loader.logging import logger
from page_loader.exceptions import HTTPError


def get_content(url, is_binary=True, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        logger.info(f'Got successful response from: {url}')
        return response.content if is_binary else response.text
    except requests.exceptions.RequestException as e:
        logger.error(f'Got unsuccessful response from {url} - {str(e)}')
        raise HTTPError()
