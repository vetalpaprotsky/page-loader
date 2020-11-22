import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def download(page_url, dir_path):
    response = requests.get(page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    image_tags = []
    for image_tag in soup.find_all('img'):
        if _is_url_relative(image_tag['src']):
            image_tags.append(image_tag)

    recources_dir_name = _url_to_name(page_url) + '_files'
    resources_dir_path = os.path.join(dir_path, recources_dir_name)
    if len(image_tags) > 0 and not os.path.isdir(resources_dir_path):
        os.mkdir(resources_dir_path)

    root_url = _get_root_url(page_url)
    for image_tag in image_tags:
        image_url = urljoin(root_url, image_tag['src'])
        image_name = _download_image(image_url, resources_dir_path)
        if image_name:
            image_tag['src'] = os.path.join(recources_dir_name, image_name)

    downloaded_page_path = os.path.join(
        dir_path, _url_to_name(page_url) + '.html'
    )
    with open(downloaded_page_path, 'w') as file:
        file.write(soup.prettify())

    return downloaded_page_path


def _url_to_name(url):
    result = urlparse(url)
    name = re.sub(r"[^0-9a-zA-Z]+", '-', result.hostname + result.path)
    return name.strip('-')


def _get_root_url(url):
    result = urlparse(url)
    return result.scheme + '://' + result.hostname


def _download_image(url, dir_path):
    response = requests.get(url)
    if response.ok:
        image_url_without_ext, ext = os.path.splitext(url)
        image_name = _url_to_name(image_url_without_ext) + ext
        image_path = os.path.join(dir_path, image_name)
        with open(image_path, 'wb') as image:
            image.write(response.content)
        return image_name


def _is_url_relative(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname is None
