===========
Schrodinger Equation 
===========


.. image:: https://travis-ci.org/tttianhao/Schrodinger.svg?branch=master
        :target: https://travis-ci.org/tttianhao/Schrodinger

.. image:: https://coveralls.io/repos/github/tttianhao/Schrodinger/badge.svg?branch=master
        :target: https://coveralls.io/github/tttianhao/Schrodinger?branch=master

Overview
--------

This project solves the lowest energy state and its wave function of a particle in a given potential field by Schrodinger Equation using Fourier basis set.
The Schrodinger Equation is:

.. image:: https://latex.codecogs.com/gif.latex?%5Cinline%20%5Chat%7BH%7D%5CPsi%28x%29%20%3D%20E%5CPsi%28x%29

where the Hamiltonian operator on a given wave function is defined as:

.. image:: https://latex.codecogs.com/gif.latex?%5Cinline%20%5Chat%20H%20%5CPsi%28x%29%3D%20-c%5Cnabla%5E2%5CPsi%28x%29&plus;V_0%28x%29


Installation
-------------

Use the following command lines to install:

``git clone https://github.com/tttianhao/Schrodinger.git``

``cd schrodinger``

``python setup.py install``

Usage
-------

Inputs:

* --size: 
        * Int, The size of the fourier basis set: {1, sin(x), cos(x), sin(2x), cos(2x)...}
        * default is 5

* --c:
        * Float, The constant in the Hamiltonian
        * default is 1

* --file:
        * String, The path and file name of the potential energy
        * default is schrodinger/potential_energy.dat
        * note: please begin the first line of the data file with "#" and the first column being position, second column being potential energy.
        * The position input has to be evenly distributed.
TODO
-------

* Revise the Hamiltonian
* Handle unevenly distributed position Inputs