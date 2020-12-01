from page_loader.download import download
from page_loader.args_parser import parse_args


def main():
    args = parse_args()
    page_path = download(args['url'], args['output'])
    print(page_path)


if __name__ == '__main__':
    main()
