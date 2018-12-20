# -*- coding: utf-8 -*-

"""Main module."""
import tensorflow as tf
import argparse
tf.enable_eager_execution()

def getParser():
    #Using parser to take in user in put form termial.
    #The default command is: schrodinger --c 1 --size 5 --file schrodinger/potential_energy.dat
    parser = argparse.ArgumentParser()
    parser.add_argument('--c', type = float, default = 1, help = 'constant c, default = 1' )
    parser.add_argument('--size', type = int, default = 5, help = 'size of the basis set, default = 5' )
    parser.add_argument('--file', type = str, default = 'schrodinger/potential_energy.dat', help = 'name of your potential energy file')
    parser.add_argument('--domain', type = str, default = None, help = 'domain, an optional parameter, default = the domain of potential energy data' )
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
    potential: list, potential energy input
    position: list, position input '''
    f = open(name, "r")
    potential = []
    position = []
    for line in f:
        if line[0] != '#':    
            position.append(float(line.split()[0]))
            potential.append(float(line.split()[1]))
    f.close()
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
        row_1 = tf.concat([row_1, tf.reshape(row_i,[n,1])],1)
    return row_1

def combine(V0, coeff, n):
    ''' This function combines the projection of V0 and the first part of the operator to get the final result

    Args:
    V0: tensor, the projection of potential energy data to basis set
    coeff: tensor, the nxn matrix of the first part of the H
    n: int, number of basis set

    returns:
    H: tensor, the matrix form of the hamlitonian
    '''
    H = V0
    for i in range(1, n):
        H = tf.concat([H, V0], 1)
    H = coeff + H
    return H

def check_domain(potential, position, domain):
    ''' This function trims the position/potential data file to fit the domain input

    Args:
    potential: list, all of the potential energy data
    position: list, all of the position data
    domain: string, user input domain 'low,high'

    returns:
    potential: list, potential data within the domain
    position: lsit, positions data within the domain
    '''
    low = float(domain.split(',')[0])
    high = float(domain.split(',')[1])
    if low < position[0] or high > position[-1] or low > high:
        raise ValueError('Check your domain input. It should be strickly within the range of position data')
    new_V0 = []
    new_x = []
    for i in range(len(position)):
        if position[i] > low and position[i] < high:
            new_x.append(position[i])
            new_V0.append(potential[i])
    return new_V0, new_x

def main():
    '''
    Main function of the project
    '''
    args = getParser()
    # Construct basis set
    basis = []
    for i in range(args.size):
        basis.append(fourier(i))
    # read potential, position data from file
    potential, position = read_file(args.file)
    # check if domain applies
    if args.domain != None:
        potential, position = check_domain(potential, position, args.domain)
    potential = tf.constant(potential, dtype = tf.float32)
    position = tf.constant(position, dtype = tf.float32)
    # calculate <V0,b>
    integration = inner_V0_b(potential,position,basis)
    integration = tf.reshape(integration,[args.size,1])
    # calculate <V0hat, b>
    coefficient = coefficient_matrix(basis,position)
    # project V0 onto basis
    solution = tf.linalg.solve(coefficient, integration)
    # project the first half of Hamltonian to basis
    matrix = operator(args.c,args.size)
    # Combine two halves of the Hamltonian
    H = combine(solution,matrix,args.size)
    # solve the eigenvector eigenvalue problem
    e,v = tf.linalg.eigh(H)
    print('Lowest energy state of the Hamiltonian: ',e[0])
    print("The wavefunction's coefficient on the basis set: ",v[0])
    return H, e[0], v[0]

if __name__ == '__main__':
    main()