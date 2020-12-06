import sys
from page_loader.download import download
from page_loader.args_parser import parse_args
from page_loader.exceptions import BaseError
from page_loader.logging import logger


def main():
    args = parse_args()
    try:
        page_file_path = download(args['url'], args['output'])
    except BaseError:
        logger.critical('Download failed')
        sys.exit(1)
    else:
        print(page_file_path)


if __name__ == '__main__':
    main()
