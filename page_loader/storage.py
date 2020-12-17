import os
import logging


def write_to_file(content, path):
    try:
        write_mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(path, write_mode) as file:
            file.write(content)
        logging.info(f'Wrote to file {path}')
    except OSError:
        logging.error(f'Failed to write to file {path}')
        raise


def create_dir(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
            logging.info(f'Created directory {path}')
    except OSError:
        logging.error(f'Failed to create directory {path}')
        raise
