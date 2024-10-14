import numpy as np

A = np.arange(12).reshape(3,4)
print(A)
#分割

'''
print(np.array_split(A,3,axis=1))
print(np.vsplit(A,3))
print(np.hsplit(A,2))
'''


#同一个数据
'''
a = np.arange(4)
print(a)
b = a
c = a
d = b
a[0] = 11
print(a)
print(b)
print(b is a)
'''

