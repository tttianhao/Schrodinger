#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `schrodinger` package."""

import pytest
import unittest
import tensorflow as tf
import math
tf.enable_eager_execution()

from schrodinger import schrodinger

class Testworkshop(unittest.TestCase):

    def test_parser(self):
        '''
        test the parser function
        '''
        args = schrodinger.getParser()
        self.assertEquals(args.file,'schrodinger/potential_energy.dat')
        self.assertEquals(args.c,1)
        self.assertEquals(args.size,5)

    def test_fourier(self):
        x = math.pi
        self.assertTrue(tf.equal(tf.constant(1,dtype=tf.float32), schrodinger.fourier(0)(x)))
        self.assertTrue(tf.equal(tf.math.sin(x), schrodinger.fourier(1)(x)))
        self.assertTrue(tf.equal(tf.math.cos(x), schrodinger.fourier(2)(x)))
        self.assertTrue(tf.equal(tf.math.cos(3*x), schrodinger.fourier(6)(x)))
        self.assertTrue(tf.equal(tf.math.sin(5*x), schrodinger.fourier(9)(x)))
        x = 3.0
        self.assertTrue(tf.equal(tf.constant(1,dtype=tf.float32), schrodinger.fourier(0)(x)))
        self.assertTrue(tf.equal(tf.math.sin(x), schrodinger.fourier(1)(x)))
        self.assertTrue(tf.equal(tf.math.cos(x), schrodinger.fourier(2)(x)))
        self.assertTrue(tf.equal(tf.math.cos(3*x), schrodinger.fourier(6)(x)))
        self.assertTrue(tf.equal(tf.math.sin(5*x), schrodinger.fourier(9)(x)))

if __name__ == '__main__':
    unittest.main()