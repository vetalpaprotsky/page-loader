import os
import re
import requests


def download(page_url, dir_path):
    response = requests.get(page_url)
    response.raise_for_status()

    file_name = _to_file_name(page_url)
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'w') as file:
        file.write(response.text)

    return file_path


def _to_file_name(page_url):
    page_url_without_scheme = re.sub(r"^.*://", '', page_url)
    file_name = re.sub(r"\W+", '-', page_url_without_scheme) + '.html'
    return file_name
