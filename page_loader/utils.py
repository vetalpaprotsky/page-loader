import os
from page_loader.logging import logger
from page_loader.exceptions import FileError, DirectoryError


def write_to_file(content, path):
    try:
        write_mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(path, write_mode) as file:
            file.write(content)
        logger.info(f'Wrote to file {path}')
    except OSError as e:
        logger.error(f'Failed to write to file {path} - {str(e)}')
        raise FileError()


def create_dir(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
            logger.info(f'Created directory {path}')
    except OSError as e:
        logger.error(f'Failed to create directory {path} - {str(e)}')
        raise DirectoryError()
