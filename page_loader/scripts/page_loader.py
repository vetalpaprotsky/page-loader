import os
from page_loader.download import download
from page_loader.args_parser import get_parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    dir_path = _get_dir_path(args.output)
    file_path = download(args.URL, dir_path)
    print(file_path)


def _get_dir_path(output):
    if output is None:
        dir_path = os.getcwd()
    elif not os.path.isabs(output):
        dir_path = os.path.join(os.getcwd(), output)
    else:
        dir_path = output
    return dir_path


if __name__ == '__main__':
    main()
