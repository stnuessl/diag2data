#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) 2024 Steffen Nuessle
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import argparse
import os
import sys
import diag2data

def file2data(infile, ext='', kind='gcc'):
    if ext == '.json':
        return diag2data.json2data(infile)
    elif ext == '.csv':
        return diag2data.csv2data(infile)
    elif kind == 'gcc' or kind == 'clang':
        return diag2data.cc2data(infile)
    elif kind == 'ghs':
        return diag2data.ghs2data(infile)
    elif kind == 'ctc':
        return diag2data.ctc2data(infile)
    else:
        return []


def data2str(data, ext='', kind='', delimiter=','):
    if ext == '.json' or kind == 'json':
        return diag2data.data2json(data)
    elif ext == '.csv' or kind == 'csv':
        return diag2data.data2csv(data, delimiter)
    elif kind == 'gcc' or kind == 'clang':
        return diag2data.data2cc(data)
    elif kind == 'ghs':
        return diag2data.data2ghs(data)
    elif kind == 'ctc':
        return diag2data.data2ctc(data)
    else:
        return diag2data.data2json(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input',
        help='',
        metavar='file',
        nargs='*',
        default=[],
        type=str
    )
    parser.add_argument(
        '--input-kind',
        help='',
        metavar='format',
        choices=(
            'clang',
            'gcc',
            'ghs',
            'ctc'
        ),
        default='gcc',
        required=False,
        type=str
    )
    parser.add_argument(
        '--output-kind',
        help='',
        metavar='format',
        choices=(
            'clang',
            'gcc',
            'ghs',
            'ctc',
            'json',
            'csv'
        ),
        default='json',
        required=False,
        type=str
    )
    parser.add_argument(
        '--reverse', '-r',
        help='',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--delimiter',
        help='',
        metavar='delimiter',
        default=',',
        required=False,
        type=str
    )
    parser.add_argument(
        '--indent',
        help='',
        metavar='',
        default='0',
        required=False,
        type=str
    )
    parser.add_argument(
        '-o',
        help='',
        metavar='file',
        default=None,
        required=False,
        type=str
    )

    args = parser.parse_args()

    diags = []

    # Process data passed via stdin
    if not sys.stdin.isatty():
        data = file2data(sys.stdin, kind=args.input_kind)

        diags.extend(data)

    # Process the data from the files passed on the command-line
    for path in args.input:
        ext = os.path.splitext(path)[1].lower()

        if args.format_in == 'csv' or ext == '.csv':
            newline = ''
        else:
            newline = None

        with open(path, 'r', newline=newline) as f:
            data = file2data(f, ext=ext, kind=args.input_kind)

            diags.extend(data)

    # Convert data to output format
    if isinstance(args.o, str):
        ext = os.path.splitext(args.o)[1]
    else:
        ext = ''


    text = data2str(data, ext, args.output_kind, args.delimiter)

    # Write the output to the appropriate file
    if args.o:
        outfile = open(args.o, 'w')
    else:
        outfile = sys.stdout

    outfile.write(text)
    outfile.close()

    sys.exit(0)

