from page_loader.download import download
from page_loader.args_parser import get_parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    file_path = download(args.URL, args.output)
    print(file_path)


if __name__ == '__main__':
    main()
