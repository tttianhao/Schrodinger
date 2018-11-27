#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `schrodinger` package."""

import pytest
import unittest

from schrodinger import schrodinger

class Testworkshop(unittest.TestCase):

    def test_parser(self):
        '''
        test the parser function
        '''
        args = schrodinger.getParser()
        self.assertEquals(args.V0,1)
        self.assertEquals(args.c,1)
        self.assertEquals(args.size,5)

if __name__ == '__main__':
    unittest.main()