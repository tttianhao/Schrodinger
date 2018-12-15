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

    def test_inner(self):
        potential = tf.constant([1,2,3,4,5],dtype=tf.float32)
        position = tf.constant([0,1,2,3,4],dtype=tf.float32)
        basis = [lambda x: tf.constant(1.), lambda x: tf.math.sin(x), lambda x: tf.math.cos(x)]
        result = schrodinger.inner_V0_b(potential,position, basis)
        A = tf.constant(15,dtype=tf.float32,shape=(1,))
        B = tf.constant(1* tf.math.sin(0.)+2*tf.math.sin(1.)+3*tf.math.sin(2.)+4*tf.math.sin(3.)+5*tf.math.sin(4.),shape=(1,))
        C = tf.constant(1* tf.math.cos(0.)+2*tf.math.cos(1.)+3*tf.math.cos(2.)+4*tf.math.cos(3.)+5*tf.math.cos(4.),shape=(1,))
        expected = tf.concat([A,B,C],0)
        print(expected)
        print(result)
        self.assertTrue(tf.equal(expected, result)[0])
        self.assertTrue(tf.equal(expected, result)[1])
        self.assertTrue(tf.equal(expected, result)[2])
if __name__ == '__main__':
    unittest.main()