#!/usr/bin/env python

import argparse
import sys
import tomllib

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        help='Path to the project\'s pyproject.toml file',
        metavar='File',
        type=str
    )
    parser.add_argument(
        '--key',
        help='The qualified path of the key for which the value is returned.',
        metavar='KEY',
        required=True,
        type=str
    )

    args = parser.parse_args()

    with open(args.path, 'rb') as tomlfile:
        data = tomllib.load(tomlfile)

        for key in args.key.split('.'):
            data = data[key]

        print(f'{data}', file=sys.stdout)

    sys.exit(0)

