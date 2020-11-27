import re
from urllib.parse import urlparse


def url_to_name(url):
    result = urlparse(url)
    name = re.sub(r"[^0-9a-zA-Z]+", '-', result.hostname + result.path)
    return name.strip('-')


def get_root_url(url):
    result = urlparse(url)
    return result.scheme + '://' + result.hostname


def is_url_local(url, root_url):
    hostname = urlparse(url).hostname
    return hostname is None or hostname == urlparse(root_url).hostname
