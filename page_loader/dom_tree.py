import os
from urllib.parse import urljoin
from page_loader.utils import (
    url_to_file_name,
    is_url_local_to_host,
    get_root_url,
)
from bs4 import BeautifulSoup


def set_local_resources(html, page_url, resources_dir_path):
    soup = BeautifulSoup(html, 'html.parser')
    root_url = get_root_url(page_url)
    resources_dir_name = os.path.split(resources_dir_path)[1]
    resources_info = []

    for tag in soup.find_all(['img', 'script', 'link']):
        resource_url = _get_resource_url(tag)
        if not (resource_url and is_url_local_to_host(resource_url, root_url)):
            continue

        full_resource_url = urljoin(root_url, resource_url)
        resource_name = url_to_file_name(full_resource_url)

        _set_resource_url(tag, os.path.join(resources_dir_name, resource_name))
        resources_info.append({
            'url': full_resource_url,
            'download_to_path': os.path.join(resources_dir_path, resource_name),
        })

    return soup.prettify(), resources_info


def _get_resource_url_attr(tag):
    if tag.name == 'img' or tag.name == 'script':
        return 'src'
    elif tag.name == 'link':
        return 'href'


def _get_resource_url(tag):
    attr = _get_resource_url_attr(tag)
    if attr:
        return tag.get(attr)


def _set_resource_url(tag, url):
    attr = _get_resource_url_attr(tag)
    if attr:
        tag[attr] = url
