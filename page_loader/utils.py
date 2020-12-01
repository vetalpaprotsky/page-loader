import os
import re
from urllib.parse import urlparse


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
        file = open(path, write_mode)
    except OSError:
        pass  # TODO log error.

    with file:
        file.write(content)


def create_dir(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except OSError:
        pass  # TODO: log error.
