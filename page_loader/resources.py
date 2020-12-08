import requests
from functools import wraps
from progress.bar import Bar
from progress.spinner import Spinner
from page_loader.logging import logger
from page_loader.exceptions import HTTPError

REQUEST_TIMEOUT = 10


def http_request(function):
    @wraps(function)
    def wrapper(url, **kwargs):
        try:
            result = function(url, **kwargs)
            logger.info(f'Got successful response from: {url}')
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f'Got unsuccessful response from {url} - {str(e)}')
            raise HTTPError()

    return wrapper


@http_request
def get_content(url, is_binary=True):
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.content if is_binary else response.text


@http_request
def get_content_by_streaming(url, is_binary=True, show_progress=False):
    response = requests.get(url, stream=True, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    CHUNK_SIZE = 256
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    content_chunks = []
    content_iterator = response.iter_content(CHUNK_SIZE)

    if show_progress:
        progress = _get_progress(url, total_size_in_bytes)
        for chunk in content_iterator:
            content_chunks.append(chunk)
            _increment_progress(progress, len(chunk))
        _finish_progress(progress)
    else:
        for chunk in content_iterator:
            content_chunks.append(chunk)

    result = b''.join(content_chunks)
    return result if is_binary else result.decode(response.encoding or 'utf-8')


def _get_progress(message, max):
    if max == 0:
        return Spinner(message + ' ')
    else:
        return Bar(message, max=max)


def _increment_progress(progress, increment_by):
    if isinstance(progress, Bar):
        progress.next(increment_by)
    else:
        progress.next()


def _finish_progress(progress):
    if isinstance(progress, Bar):
        progress.goto(progress.max)
    progress.finish()
