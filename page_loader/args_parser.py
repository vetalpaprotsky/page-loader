import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('URL', type=str)
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='directory path where page will be saved'
    )
    return parser
