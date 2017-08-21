import numpy as np

[1] * 5
a = np.array(((3,2),(2,3)))

print a[1,:]


np.save('arre.npy',a)
b = np.load('arre.npy')
