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
        return lambda x: tf.math.cos((n//2)*x)-tf.math.cos((n//2)*x)+1
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

def inner_V0hat_b(basis, position,basisn):
    ''' This function evalutes the innver product of <V0hat, bn> where bn is the nth vector in the basis

    Args:
    basis: list, the basis set user chosen
    position: tensor, the position input by user
    basisn: the nth vector in the basis set

    returns:
    result: tensor, the matrix of coefficient of the system of equation used to solve basis vector coefficient
    '''
    for i in range(len(basis)):
        coefficientij = tf.constant(tf.reduce_sum(basis[i](position)*tf.transpose(basisn(position))),shape=[1,])
        try:
            coefficienti
        except NameError:
            coefficienti = coefficientij
        else:
            coefficienti = tf.concat([coefficienti, coefficientij],0)
    return tf.reshape(coefficienti,[len(basis),1])

def coefficient_matrix(basis, position):
    ''' This function evalutes the innver product of <V0hat, b> by numerical integration

    Args:
    basis: list, the basis set user chosen
    position: tensor, the position input by user

    returns:
    result: tensor, the matrix of coefficient of the system of equation used to solve basis vector coefficient
    '''
    for i in basis:
        coefficienti = inner_V0hat_b(basis, position, i)
        try:
            coefficient
        except NameError:
            coefficient = coefficienti
        else:
            coefficient = tf.concat([coefficient, coefficienti],1)
    return coefficient

def operator(c,n):
    ''' This function construct the matrix form of the operator

    Args:
    c: float, the constant of user input
    n: int, the number of desired basis set

    returns:
    matrix: tensor, the matrix form of the operator
    '''
    row_1 = tf.constant(tf.zeros(n),shape=(n,1),dtype=tf.float32)
    for i in range(1,n):
        start = True
        for j in range(0,n):
            if i!= j:
                matrix_ij = tf.constant(0,dtype=tf.float32,shape=(1,))
            else:
                matrix_ij = tf.constant(c*((i+1)//2)**2,dtype=tf.float32,shape=(1,))
            if start:
                row_i = matrix_ij
                start = False
            else:
                row_i = tf.concat([row_i, matrix_ij],0)
        row_1 = tf.concat([row_1, tf.reshape(row_i,[5,1])],1)
    return row_1

def main():
    args = getParser()
    n = args.size
    basis = []
    for i in range(n):
        basis.append(fourier(i))
    potential, position = read_file(args.file)
    print('positions are ',position)
    print('potentials are ',potential)
    integration = inner_V0_b(potential,position,basis)
    integration = tf.reshape(integration,[len(basis),1])
    print('integration are ',integration)
    coefficient = coefficient_matrix(basis,position)
    print(coefficient)
    solution = tf.linalg.solve(coefficient, integration)
    print(solution)
    matrix = operator(1,5)
    print(matrix)

if __name__ == '__main__':
    main()