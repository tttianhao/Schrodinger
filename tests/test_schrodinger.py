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

    def test_readfile(self):
        potential, position = schrodinger.read_file('schrodinger/potential_energy.dat')
        print(tf.shape(potential))
        print(tf.shape(position))
        self.assertTrue(tf.equal(tf.shape(potential),tf.shape(position))[0])
    
    def test_inner2(self):
        basis = [lambda x: tf.math.cos((9//2)*x)-tf.math.cos((9//2)*x)+1, lambda x: tf.math.sin(x), lambda x: tf.math.cos(x)]
        position = tf.constant([0,1,2,3,4],dtype=tf.float32)
        A = tf.constant(5,dtype=tf.float32,shape=(1,))
        B = tf.constant(tf.reduce_sum(basis[1](position)),shape=(1,))
        C = tf.constant(tf.reduce_sum(basis[2](position)),shape=(1,))
        expected = tf.concat([A,B,C],0)
        result = schrodinger.inner_V0hat_b(basis,position,basis[0])
        expected = tf.reshape(expected,[3,1])
        self.assertTrue(tf.equal(expected, result)[0][0])
        self.assertTrue(tf.equal(expected, result)[1][0])
        self.assertTrue(tf.equal(expected, result)[2][0])
        
    def test_coeffmatrix(self):
        basis = [lambda x: tf.math.cos((9//2)*x)-tf.math.cos((9//2)*x)+1, lambda x: tf.math.sin(x), lambda x: tf.math.cos(x)]
        position = tf.constant([0,1,2,3,4],dtype=tf.float32)
        A = tf.constant(5,dtype=tf.float32,shape=(1,))
        B = tf.constant(tf.reduce_sum(basis[1](position)),shape=(1,))
        C = tf.constant(tf.reduce_sum(basis[2](position)),shape=(1,))
        D = tf.constant(tf.reduce_sum(basis[1](position)*tf.transpose(tf.constant(tf.math.sin(position)))),shape=(1,))
        expected = tf.concat([A,B,C,tf.constant(0.,shape=(1,)),D,tf.constant(0.,shape=(1,)),tf.constant(0.,shape=(1,)),tf.constant(0.,shape=(1,)),tf.constant(0.,shape=(1,))],0)
        result = schrodinger.coefficient_matrix(basis,position)
        self.assertTrue(tf.equal(tf.shape(result)[0],tf.constant(3)))
        self.assertTrue(tf.equal(tf.shape(result)[1],tf.constant(3)))
        expected = tf.reshape(expected,[9,1])
        result = tf.reshape(result,[9,1])
        self.assertTrue(tf.equal(expected, result)[0][0])
        self.assertTrue(tf.equal(expected, result)[1][0])
        self.assertTrue(tf.equal(expected, result)[2][0])
        self.assertTrue(tf.equal(expected, result)[4][0])

    def test_operator(self):
        result = schrodinger.operator(10, 10)
        self.assertTrue(tf.equal(result[0][0], tf.constant(0.)))
        self.assertTrue(tf.equal(result[6][6], tf.constant(90.)))
        self.assertTrue(tf.equal(result[5][5], tf.constant(90.)))
        self.assertTrue(tf.equal(result[1][0], tf.constant(0.)))
    
    def test_combine(self):
        V0 = tf.constant([0,1,2,3,4],shape=(5,1),dtype=tf.float32)
        coef = tf.constant(tf.zeros(25),shape=(5,5),dtype=tf.float32)
        result = schrodinger.combine(V0,coef,5)
        self.assertTrue(tf.equal(tf.shape(result)[0],tf.constant(5)))
        self.assertTrue(tf.equal(tf.shape(result)[1],tf.constant(5)))
        for i in [0,1,2,3,4]:
            expected = tf.constant(i,dtype=tf.float32,shape=())
            self.assertTrue(tf.equal(expected, result[i][0]))

    def test_checkdomain(self):
        V0 = [0,1,2,3,4,5]
        x = [0,1,2,3,4,5]
        domain = '2,4'
        potential, position = schrodinger.check_domain(V0,x,domain)
        self.assertEqual(potential,[2,3,4])
        self.assertEqual(position,[2,3,4])
        domain = '0.5,4.5'
        potential, position = schrodinger.check_domain(V0,x,domain)
        self.assertEqual(potential,[1,2,3,4])
        self.assertEqual(position,[1,2,3,4])
        with pytest.raises(ValueError) as e:
            domain = '0.5,120'
            schrodinger.check_domain(V0,x,domain)
        self.assertEqual(str(e.value), 'Check your domain input. It should be strickly within the range of position data')

    def test_main(self):
        H, value, vector = schrodinger.main()
        five = tf.constant(5, dtype=tf.int32)
        self.assertTrue(tf.equal(tf.shape(H)[0],five))
        self.assertTrue(tf.equal(tf.shape(vector)[0],five))
        
if __name__ == '__main__':
    unittest.main()