import os
from page_loader.logging import logger
from page_loader.exceptions import FileError, HTTPError
from page_loader.resource import get_resource_content
from page_loader.dom_tree import set_local_resources
from page_loader.utils import (
    url_to_name,
    url_to_file_name,
    create_file,
    create_dir,
)


def download(page_url, output_dir_path):
    page_html = get_resource_content(page_url, is_binary=False)

    resources_dir_path = os.path.join(
        output_dir_path,
        url_to_name(page_url) + '_files',
    )
    updated_page_html, resources_info = set_local_resources(
        page_html,
        page_url,
        resources_dir_path,
    )

    if len(resources_info) > 0:
        create_dir(resources_dir_path)
        for info in resources_info:
            _download_resource(info['url'], info['download_to_path'])

    page_file_path = os.path.join(
        output_dir_path,
        url_to_file_name(page_url),
    )
    create_file(updated_page_html, page_file_path)

    return page_file_path


def _download_resource(url, download_to_path):
    try:
        content = get_resource_content(url)
        create_file(content, download_to_path)
    except (HTTPError, FileError) as e:
        logger.warning(f"Resource {url} wasn't downloaded - {str(e)}")
