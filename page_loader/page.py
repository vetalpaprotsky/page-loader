import os
import requests
import page_loader.recourse as recourse
from bs4 import BeautifulSoup
from page_loader.utils import is_url_local, url_to_name, get_root_url
from urllib.parse import urljoin


def download(page_url, output_dir_path):
    response = requests.get(page_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    root_url = get_root_url(page_url)
    tags = _get_tags_with_local_resources(soup, root_url)

    resources_dir_name = url_to_name(page_url) + '_files'
    resources_dir_path = os.path.join(output_dir_path, resources_dir_name)
    if len(tags) > 0 and not os.path.isdir(resources_dir_path):
        os.mkdir(resources_dir_path)

    for tag in tags:
        full_resource_url = urljoin(root_url, tag['soup'][tag['attr']])
        resource_name = recourse.download(
            full_resource_url,
            resources_dir_path
        )
        if resource_name:
            tag['soup'][tag['attr']] = os.path.join(
                resources_dir_name, resource_name
            )

    page_path = os.path.join(output_dir_path, url_to_name(page_url) + '.html')
    with open(page_path, 'w') as file:
        file.write(soup.prettify())

    return page_path


def _get_tags_with_local_resources(soup, root_url):
    tags = []
    for tag in soup.find_all(['img', 'link', 'script']):
        if (
            (tag.name == 'img' or tag.name == 'script')
            and tag.get('src') is not None
            and is_url_local(tag['src'], root_url)
        ):
            tags.append({'soup': tag, 'attr': 'src'})
        elif (
            tag.name == 'link'
            and tag.get('href') is not None
            and is_url_local(tag['href'], root_url)
        ):
            tags.append({'soup': tag, 'attr': 'href'})
    return tags
