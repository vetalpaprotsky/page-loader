import requests
from page_loader.logging import logger


def get_resource_content(url, is_binary=True):
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info(f'Successfully got resource from: {url}')
        return response.content if is_binary else response.text
    except requests.exceptions.HTTPError:
        logger.error(f'Failed to get resource from: {url}')
        raise
