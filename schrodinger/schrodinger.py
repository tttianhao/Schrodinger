# -*- coding: utf-8 -*-

"""Main module."""
import tensorflow as tf
import argparse
import numpy as np
import math
tf.enable_eager_execution()

def getParser():
    #Using parser to take in user in put form termial.
    #The default command is:
    parser = argparse.ArgumentParser()
    parser.add_argument('--V0', type = float, default = 1, help = 'potential energy, defaul = 1' )
    parser.add_argument('--c', type = float, default = 1, help = 'constant c, default = 1' )
    parser.add_argument('--size', type = int, default = 5, help = 'size of the basis set, default = 5' )
    #parser.add_argument('--wave', )
    args = parser.parse_args()
    return args

def pro(x):
    return x**2 + 3

def main():
    # array_1 = tf.constant(tf.lin_space(0,100,101),dtype=tf.float64)
    print(tf.__version__)
    array_1 = tf.lin_space(0.,100.,101)
    print(array_1)
    # a=tf.ones((1,3))
    # b=tf.ones((1,3))
    # x = b#tf.Variable(b)
    # var2=tf.matmul(tf.ones((1,3)),tf.ones((3,2)))
    # var1=tf.linalg.cross(a,x)
    # print(a,b,var2,var1)

if __name__ == '__main__':
    main()