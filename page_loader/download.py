import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def download(page_url, output_dir_path):
    response = requests.get(page_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    root_url = _get_root_url(page_url)
    tags = _get_tags_with_local_resources(soup, root_url)

    resources_dir_name = _url_to_name(page_url) + '_files'
    resources_dir_path = os.path.join(output_dir_path, resources_dir_name)
    if len(tags) > 0 and not os.path.isdir(resources_dir_path):
        os.mkdir(resources_dir_path)

    for tag in tags:
        full_resource_url = urljoin(root_url, tag['soup'][tag['attr']])
        resource_name = _download_resourse(
            full_resource_url,
            resources_dir_path
        )
        if resource_name:
            tag['soup'][tag['attr']] = os.path.join(
                resources_dir_name, resource_name
            )

    page_path = os.path.join(output_dir_path, _url_to_name(page_url) + '.html')
    with open(page_path, 'w') as file:
        file.write(soup.prettify())

    return page_path


def _url_to_name(url):
    result = urlparse(url)
    name = re.sub(r"[^0-9a-zA-Z]+", '-', result.hostname + result.path)
    return name.strip('-')


def _get_root_url(url):
    result = urlparse(url)
    return result.scheme + '://' + result.hostname


def _download_resourse(url, dir_path):
    response = requests.get(url)
    if response.ok:
        resourse_url_without_ext, ext = os.path.splitext(url)
        if not ext:
            ext = '.html'
        resourse_name = _url_to_name(resourse_url_without_ext) + ext
        resourse_path = os.path.join(dir_path, resourse_name)
        with open(resourse_path, 'wb') as resourse:
            resourse.write(response.content)
        return resourse_name


def _is_url_local(url, root_url):
    hostname = urlparse(url).hostname
    return hostname is None or hostname == urlparse(root_url).hostname


def _get_tags_with_local_resources(soup, root_url):
    tags = []
    for tag in soup.find_all(['img', 'link', 'script']):
        if (
            (tag.name == 'img' or tag.name == 'script')
            and tag.get('src') is not None
            and _is_url_local(tag['src'], root_url)
        ):
            tags.append({'soup': tag, 'attr': 'src'})
        elif (
            tag.name == 'link'
            and tag.get('href') is not None
            and _is_url_local(tag['href'], root_url)
        ):
            tags.append({'soup': tag, 'attr': 'href'})
    return tags


# TODO: create some file which will contain some abstract functions which
# interact with the soup tree and its tags.
