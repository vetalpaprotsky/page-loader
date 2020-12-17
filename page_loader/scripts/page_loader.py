import sys
import logging
import page_loader.logging
from page_loader.downloading import download
from page_loader.args_parsing import parse_args


def main():
    page_loader.logging.setup()
    args = parse_args()
    try:
        page_file_path = download(args['url'], args['output'])
    except Exception as e:
        logging.critical(f'Download failed - {str(e)}')
        sys.exit(1)
    else:
        print(f'Page was downloaded as {page_file_path}')


if __name__ == '__main__':
    main()
