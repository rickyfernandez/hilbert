import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

key_index_2d = [0, 1, 3, 2]
key_index_3d = [0, 1, 7, 6, 3, 2, 4, 5]

def hilbert_key_2d(x,y,order):

    key = 0
    for i in range(order-1, -1, -1):

        xbit = 1 if x & (1 << i) else 0
        ybit = 1 if y & (1 << i) else 0

        if   xbit == 0 and ybit == 0: x, y = y, x
        elif xbit == 1 and ybit == 0: x, y = ~y, ~x

        key = (key << 2) + key_index_2d[(xbit << 1) + ybit]

    return key

def hilbert_key_3d(x,y,z,order):

    key = 0
    for i in range(order-1, -1, -1):

        xbit = 1 if x & (1 << i) else 0
        ybit = 1 if y & (1 << i) else 0
        zbit = 1 if z & (1 << i) else 0

        if   xbit == 0 and ybit == 0 and zbit == 0: y, z = z, y
        elif xbit == 0 and ybit == 0 and zbit == 1: x, y = y, x
        elif xbit == 1 and ybit == 0 and zbit == 1: x, y = y, x
        elif xbit == 1 and ybit == 0 and zbit == 0: x, z = ~x, ~z
        elif xbit == 1 and ybit == 1 and zbit == 0: x, z = ~x, ~z
        elif xbit == 1 and ybit == 1 and zbit == 1: x, y = ~y, ~x
        elif xbit == 0 and ybit == 1 and zbit == 1: x, y = ~y, ~x
        elif xbit == 0 and ybit == 1 and zbit == 0: y, z = ~z, ~y

        key = (key << 3) + key_index_3d[(xbit << 2) + (ybit << 1) + zbit]

    return key

def key_neighbors_in_range_2d(x, y, a_key, b_key, order):

    for i in  [-1, 0, 1]:
        for j in  [-1, 0, 1]:

            xn = x + i; yn = y + j

            # border particles
            if xn < 0 or xn > 2**order: return True
            if yn < 0 or yn > 2**order: return True

            # cpu neighbor particles
            key = hilbert_key_2d(xn, yn, order)
            if key < a_key or key > b_key: return True

    return False


if __name__ == "__main__":

    dimension = int(raw_input("Enter the dimension: "))
    order = int(raw_input("Enter the order of the hilbert curve: "))

    if dimension == 2:

        num_points = 2**order
        points = [(x,y) for x in range(num_points) for y in range(num_points)]
        sorted_points = np.array(sorted(points, key=lambda k: hilbert_key_2d(k[0], k[1], order)))
        plt.plot(sorted_points[:,0], sorted_points[:,1], 'r')

        plt.xlim(-0.5, num_points -1 + .5)
        plt.ylim(-0.5, num_points -1 + .5)
        plt.yticks(np.arange(0.5, num_points -1 + .5), [])
        plt.xticks(np.arange(0.5, num_points -1 + .5), [])
        plt.grid()
        plt.show()

    if dimension == 3:

        num_points = 2**order
        points = [(x,y,z) for x in range(num_points) \
                for y in range(num_points) \
                for z in range(num_points)]

        sorted_points = np.array(sorted(points, key=lambda k: hilbert_key_3d(k[0], k[1], k[2], order)))

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot(sorted_points[:,0], sorted_points[:,1], sorted_points[:,2], 'r')
        plt.show()
