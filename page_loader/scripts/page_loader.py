import sys
from page_loader.downloading import download
from page_loader.args_parsing import parse_args
from page_loader.logging import logger


def main():
    args = parse_args()
    try:
        page_file_path = download(args['url'], args['output'])
    except Exception as e:
        logger.critical(f'Download failed - {str(e)}')
        sys.exit(1)
    else:
        print(f'Page was downloaded as {page_file_path}')


if __name__ == '__main__':
    main()
