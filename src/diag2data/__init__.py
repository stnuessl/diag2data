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

import csv
import io
import json
import re
import sys

def cc2data(infile):
    data = []

    regex_line = re.compile(
        r'^(?P<path>[^:]+)'
        r':'
        r'(?P<line>\d+)'
        r':'
        r'(?P<column>\d+)'
        r': '
        r'(?P<severity>[^:]+)'
        r': '
        r'(?P<message>.*)'
    )

    regex_diag = re.compile(
        r' \[(?P<diagnostic>[^\]]+)\]'
    )

    for line in infile:
        if match := regex_line.match(line):
            item = {
                'Path' : match.group('path'),
                'Line' : match.group('line'),
                'Column' : match.group('column'),
                'Severity' : match.group('severity'),
                'Message' : '',
                'Diagnostic' : '',
            }

            message = match.group('message')

            if match := regex_diag.search(message):
                item['Message'] = message[:match.start()]
                item['Diagnostic'] = match.group('diagnostic')
            else:
                item['Message'] = message


            data.append(item)

    return data

def ghs2data(infile):
    data = []
    regex = re.compile(
        r'"(?P<path>[^"]+)"'
        r', line '
        r'(?P<line>\d+)'
        r'( \(col. (?P<column>\d+)\))?'
        r': '
        r'(?P<severity>[^ :]+)'
        r'( (?P<diagnostic>[^:]+))?'
        r': '
        r'(?P<message>.*)'
    )

    for line in infile:
        if match := regex.match(line):
            if not (column := match.group('column')):
                column = '0'

            if not (diagnostic := match.group('diagnostic')):
                diagnostic = ''

            item = {
                'Path' : match.group('path'),
                'Line' : match.group('line'),
                'Column' : column,
                'Severity' : match.group('severity'),
                'Message' : match.group('message'),
                'Diagnostic' : diagnostic,
            }

            data.append(item)

    return data

def ctc2data(infile):
    data = []

    regex = re.compile(
        r'^\w+'
        r' '
        r'(?P<diagnostic>[FEWIS]\d+)'
        r': \['
        r'"(?P<path>[^"]+)"'
        r' '
        r'(?P<line>\d+)'
        r'/'
        r'(?P<column>\d+)'
        r'\] '
        r'(?P<message>.*)'
    )

    severity = {
        'F' : 'fatal',
        'E' : 'error',
        'W' : 'warning',
        'I' : 'note',
        'S' : 'system error'
    }

    for line in infile:
        if match := regex.match(line):
            diag = match.group('diagnostic')

            item = {
                'Path' : match.group('path'),
                'Line' : match.group('line'),
                'Column' : match.group('column'),
                'Severity' : severity[diag[0]],
                'Message' : match.group('message'),
                'Diagnostic' : diag,
            }

            data.append(item)

    return data

def json2data(infile):
    return json.load(infile)

def csv2data(infile):
    dialect = csv.Sniffer().sniff(next(infile))
    infile.seek(0)

    return [x for x in csv.DictReader(infile, dialect=dialect)]


def data2cc(data):
    f = io.StringIO()

    for diag in data:
        f.write(diag['Path'])
        f.write(':')
        f.write(diag['Line'])
        f.write(':')
        f.write(diag['Column'])
        f.write(': ')
        f.write(diag['Severity'])
        f.write(': ')
        f.write(diag['Message'])

        if diag['Diagnostic']:
            f.write(' [')
            f.write(diag['Diagnostic'])
            f.write(']')

        f.write('\n')

    return f.getvalue()

def data2ghs(data):
    f = io.StringIO()

    for diag in data:
        '"main.c", line 999 (col. 22): warning #186-D: pointless comparison of unsigned integer with zero',
        f.write('"')
        f.write(diag['Path'])
        f.write('", line ')
        f.write(diag['Line'])

        if diag['Column'] != '0':
            f.write(' (col. ')
            f.write(diag['Column'])
            f.write(')')

        f.write(': ')
        f.write(diag['Severity'])

        if diag['Diagnostic']:
            f.write(' ')
            f.write(diag['Diagnostic'])

        f.write(': ')
        f.write(diag['Message'])
        f.write('\n')

    return f.getvalue()

def data2ctc(data):
    f = io.StringIO()

    regex = re.compile(r'[FEWIS][0-9]+')

    diagnostic_mapping = {
        'fatal' : 'F000',
        'error' : 'E000',
        'warning' : 'W000',
        'note' : 'I000',
    }

    for diag in data:
        f.write('ctc ')

        if regex.match(diag['Diagnostic']):
            f.write(diag['Diagnostic'])
        else:
            severity = diag['Severity']
            f.write(diagnostic_mapping[severity])

        f.write(': ["')
        f.write(diag['Path'])
        f.write('" ')
        f.write(diag['Line'])
        f.write('/')
        f.write(diag['Column'])
        f.write('] ')
        f.write(diag['Message'])
        f.write('\n')

    return f.getvalue()


def data2csv(data, delimiter=','):
    f = io.StringIO(newline='')

    if data:
        csvopts = {
            'fieldnames' : data[0].keys(),
            'quoting' : csv.QUOTE_ALL,
            'delimiter' : delimiter,
        }

        writer = csv.DictWriter(f, **csvopts)

        writer.writeheader()
        writer.writerows(data)

    return f.getvalue()

def data2json(data, indent=4):
    f = io.StringIO()

    json.dump(data, f, indent=indent)

    if indent != 0:
        f.write('\n')

    return f.getvalue()
