#!/usr/bin/env python

import io
import os
import unittest
import json

import diag2data


class Tester(unittest.TestCase):
    def setUp(self):
        dirname = os.path.dirname(__file__)
        self.input = open(f'{dirname}/gcc-diagnostics.txt', 'r')

        with open(f'{dirname}/expected-gcc.json', 'r') as infile:
            self.expected = json.load(infile)

    def tearDown(self):
        self.input.close()

    def test_cc2data(self):
        data = diag2data.cc2data(self.input)

        self.assertEqual(self.expected, data)

    def test_cc2json(self):
        data = diag2data.cc2data(self.input)

        text = diag2data.data2json(data)
        s = io.StringIO(text)
        data = diag2data.json2data(s)

        self.assertEqual(self.expected, data)

    def test_cc2csv(self):
        data = diag2data.cc2data(self.input)

        text = diag2data.data2csv(data)

        s = io.StringIO(text, newline='')
        data = diag2data.csv2data(s)

        self.assertEqual(self.expected, data)

    def test_cc2cc(self):
        data = diag2data.cc2data(self.input)

        text = diag2data.data2cc(data)

        s = io.StringIO(text)
        data = diag2data.cc2data(s)

        self.assertEqual(self.expected, data)

    def test_cc2ghs(self):
        data = diag2data.cc2data(self.input)

        text = diag2data.data2ghs(data)

        s = io.StringIO(text)
        data = diag2data.ghs2data(s)

        self.assertEqual(self.expected, data)

    def test_cc2ctc(self):
        data = diag2data.cc2data(self.input)

        text = diag2data.data2ctc(data)

        s = io.StringIO(text)
        data = diag2data.ctc2data(s)

        self.assertEqual(len(self.expected), len(data))

        for i in range(len(data)):
            for field in data[i]:
                if field == 'Diagnostic':
                    continue

                self.assertEqual(self.expected[i][field], data[i][field])


if __name__ == '__main__':
    unittest.main()
