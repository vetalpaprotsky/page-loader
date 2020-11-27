import os
import requests
from page_loader.utils import url_to_name


def download(url, dir_path):
    response = requests.get(url)
    if response.ok:
        resourse_url_without_ext, ext = os.path.splitext(url)
        if not ext:
            ext = '.html'
        resourse_name = url_to_name(resourse_url_without_ext) + ext
        resourse_path = os.path.join(dir_path, resourse_name)
        with open(resourse_path, 'wb') as resourse:
            resourse.write(response.content)
        return resourse_name
