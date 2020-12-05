import os
import re
from urllib.parse import urlparse
from page_loader.logging import logger
from page_loader.exceptions import FileError, DirectoryError


def url_to_name(url):
    result = urlparse(url)
    name = re.sub(r"[^0-9a-zA-Z]+", '-', result.hostname + result.path)
    return name.strip('-')


def url_to_file_name(url, default_ext='.html'):
    url = url.rstrip('/')
    _, ext = os.path.splitext(urlparse(url).path)
    if not ext:
        url_without_ext = url
        ext = default_ext
    else:
        url_without_ext = url[0:-len(ext)]
    return url_to_name(url_without_ext) + ext


def get_root_url(url):
    result = urlparse(url)
    return result.scheme + '://' + result.hostname


def is_url_local_to_host(url, root_url):
    hostname = urlparse(url).hostname
    return hostname is None or hostname == urlparse(root_url).hostname


def create_file(content, path):
    try:
        write_mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(path, write_mode) as file:
            file.write(content)
        logger.info(f'Created file: {path}')
    except OSError as e:
        logger.error(f'Failed to create file: {path}')
        raise FileError(str(e))


def create_dir(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
            logger.info(f'Created directory: {path}')
    except OSError as e:
        logger.error(f'Failed to create directory: {path}')
        raise DirectoryError(str(e))
