import os
import argparse


def parse_args():
    parser = _get_parser()
    args = parser.parse_args()
    if not os.path.isabs(args.output):
        output = os.path.join(os.getcwd(), args.output)
    else:
        output = args.output
    return {'url': args.url, 'output': output}


def _get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str)
    parser.add_argument(
        '-o', '--output',
        metavar='dir',
        type=str,
        help='output dir (default is the current directory)',
        default=os.getcwd(),
    )
    return parser
