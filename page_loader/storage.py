import os
import logging
from page_loader.exceptions import PageLoadingError


def write_to_file(content, path):
    try:
        write_mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(path, write_mode) as file:
            file.write(content)
        logging.info(f'Wrote to file {path}')
    except OSError as e:
        raise PageLoadingError(f'Failed to write to file {path}') from e


def create_dir(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
            logging.info(f'Created directory {path}')
    except OSError as e:
        raise PageLoadingError(f'Failed to create directory {path}') from e
