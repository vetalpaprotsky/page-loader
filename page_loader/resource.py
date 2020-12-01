import requests


def get_resource_content(url, is_binary=True):
    response = requests.get(url)
    if response.ok:
        return response.content if is_binary else response.text
    else:
        pass  # TODO: log error.
