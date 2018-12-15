# -*- coding: utf-8 -*-

"""Main module."""
import tensorflow as tf
import argparse
import math
tf.enable_eager_execution()

def getParser():
    #Using parser to take in user in put form termial.
    #The default command is:
    parser = argparse.ArgumentParser()
    parser.add_argument('--c', type = float, default = 1, help = 'constant c, default = 1' )
    parser.add_argument('--size', type = int, default = 5, help = 'size of the basis set, default = 5' )
    parser.add_argument('--file', type = str, default = 'schrodinger/potential_energy.dat', help = 'name of your potential energy file')
    args = parser.parse_args()
    return args

def fourier(n):
    ''' This function returns the nth element in the basis set

    Args:
    n: int, the nth element in the fourier series

    returns:
    fourier: function. the nth vector in the basis set '''
    if n == 0:
        return lambda x: tf.constant(1,dtype=tf.float32)
    elif n % 2 == 1: #sinnx
        return lambda x: tf.math.sin(((n//2)+1)*x)
    return lambda x: tf.math.cos((n//2)*x) #cosnx

def read_file(name):
    ''' This funciton extract potential energy and position data from the data file.

    Args:
    name: String, file name of the potential energy of the data file

    returns:
    potential: tensor, potential energy input
    position: tensor, position input '''
    f = open(name, "r")
    potential = []
    position = []
    for line in f:
        if line[0] != '#':    
            position.append(float(line.split()[0]))
            potential.append(float(line.split()[1]))
    f.close()
    potential = tf.constant(potential, dtype = tf.float32)
    position = tf.constant(position, dtype = tf.float32)
    return potential, position

def inner_V0_b(potential, position, fourier):
    ''' This function calculates the inner product of <V0, b> by numerical integration

    Args:
    potential, position: tensor, potential energy and position input from user
    fourier: tensor, the basis set of first n terms of fourier transform

    returns:
    result: tensor, the result of numerical integration'''
    result = tf.reduce_sum(fourier[0](position) * tf.transpose(potential))
    result = tf.constant(result,shape=[1,])
    for i in range(1,len(fourier)):
        integral = tf.reduce_sum(fourier[i](position) * tf.transpose(potential))
        integral = tf.constant(integral,shape=[1,])
        result = tf.concat([result,integral],0)
    return result

def main():
    print(1//2)
    args = getParser()
    n = args.size
    basis = []
    for i in range(n):
        basis.append(fourier(i))
    potential, position = read_file(args.file)
    print('positions are ',position)
    print('potentials are ',potential)
    integration = inner_V0_b(potential,position,basis)
    print(integration)
if __name__ == '__main__':
    main()