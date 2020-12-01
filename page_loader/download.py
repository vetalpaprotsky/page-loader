import os
from page_loader.resource import get_resource_content
from page_loader.dom_tree import set_local_resources
from page_loader.utils import (
    url_to_name,
    url_to_resource_name,
    create_dir,
    write_to_file,
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
            content = get_resource_content(info['url'])
            write_to_file(content, info['download_to_path'])

    page_path = os.path.join(
        output_dir_path,
        url_to_resource_name(page_url),
    )
    write_to_file(updated_page_html, page_path)

    return page_path
