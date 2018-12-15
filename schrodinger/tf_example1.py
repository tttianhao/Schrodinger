import tensorflow as tf
from tensorflow import linalg
#import numpy as np
import math
#mnist = tf.keras.datasets.mnist


tf.enable_eager_execution()

a=tf.ones((1,3))
b=tf.ones((1,3))
x = b#tf.Variable(b)
var2=tf.matmul(tf.ones((1,3)),tf.ones((3,2)))
var1=tf.linalg.cross(a,x)
print(a,b,var2,var1)

print(tf.add(1, 2))
print(tf.add([1, 2], [3, 4]))
print(tf.square(5))
print(tf.reduce_sum([1, 2, 3]))

print(tf.encode_base64("hello world"))
print(tf.square(2) + tf.square(3))

x2 = tf.matmul([[5,6,7]], [[6],[ 7],[90]])
print(x2.shape)
print(x2.dtype)
print(x2)

real = tf.constant([2.25, 3.25])
imag = tf.constant([4.75, 5.75])
yy=tf.complex(real, imag)  # [[2.25 + 4.75j], [3.25 + 5.75j]]
print(yy)

real2 = tf.constant([2.25])
imag2 = tf.constant([4.75])
yy2=tf.complex(real2, imag2)  # [[2.25 + 4.75j], [3.25 + 5.75j]]
x =tf.complex([5.0,8],[6.0,7])

print(x,yy,yy2)
array_1=tf.constant(tf.range(1,21,1),shape=[5,4], dtype=tf.int32)
array_2=tf.constant(tf.range(21,41,1),shape=[4,5], dtype=tf.int32)
print(array_1,array_2)


print(tf.linalg.matmul(array_1,array_2))

a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0,7.0,8.0,9.0], shape=[3, 3],dtype=tf.float64)


b = tf.constant([7, 8, 9, 10, 11, 12,13,14.0,15], shape=[3, 3],dtype=tf.float64)

print(a,b)
c = tf.matmul(a, b)
print(c,a)


### Getting the diagonal matrix of the matrix ###
determinant_a=tf.linalg.det(a)

mat_determinant_a=tf.matrix_determinant(a)
print(tf.executing_eagerly())
print(determinant_a,mat_determinant_a)
print(1*5*9+2*6*7+3*4*8-7*5*3-8*6*1-9*4*2)

matr=tf.constant([1,1,1,-1],shape=[2,2],dtype=tf.float64)
print(tf.linalg.solve(matr, rhs=tf.constant([[9],[-1]],dtype=tf.float64),adjoint=True))


