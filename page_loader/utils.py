import os
import re
from urllib.parse import urlparse
from page_loader.logging import logger


def url_to_name(url):
    result = urlparse(url)
    name = re.sub(r"[^0-9a-zA-Z]+", '-', result.hostname + result.path)
    return name.strip('-')


def url_to_file_name(url, default_ext='.html'):
    url_without_ext, ext = os.path.splitext(url)
    if not ext:
        ext = default_ext
    return url_to_name(url_without_ext) + ext


def get_root_url(url):
    result = urlparse(url)
    return result.scheme + '://' + result.hostname


def is_url_local_to_host(url, root_url):
    hostname = urlparse(url).hostname
    return hostname is None or hostname == urlparse(root_url).hostname


def write_to_file(content, path):
    try:
        write_mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(path, write_mode) as file:
            file.write(content)
        logger.info(f'Created file: {path}')
    except OSError as e:
        logger.error(f'Failed to write to a file: {str(e)}')
        raise


def create_dir(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
            logger.info(f'Created directory: {path}')
    except OSError as e:
        logger.error(f'Failed to create a directory: {str(e)}')
        raise
