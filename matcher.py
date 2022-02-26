import numpy as np
import random
path = 'datasets/water/'
name = 'water'
npy = '.npy'

data = np.load(path + name + npy)
categories = np.load(path + name + "_categories" + npy)
print(data)
print(categories)

num_of_sets = 100
num_of_vectors  = 6
num_of_entries = 4
result = np.zeros((num_of_sets, num_of_vectors, num_of_entries))
for i in range(num_of_sets):
    for j in range(num_of_vectors):
        idx = random.randint(0, len(data) - 1)
        result[i][j] = data[idx]

np.save(path + name+"_sets.npy", result)