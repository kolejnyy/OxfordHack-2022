import numpy as np
import random
path = 'datasets/nba/'
name = 'nba'
npy = '.npy'

data = np.load(path + name + npy, allow_pickle=True)
categories = np.load(path + name + "_categories" + npy, allow_pickle=True)
print(data)
print(categories)

num_of_sets = 100
num_of_vectors  = 6
num_of_entries = 4
N = len(data)
result = np.zeros((num_of_sets, num_of_vectors, num_of_entries)).astype(object)

def rng_idx():
    return random.randint(0, N - 1)

def random_match():
    for i in range(num_of_sets):
        for j in range(num_of_vectors):
            idx = rng_idx()
            result[i][j] = data[idx]

def similarity_match():
    np.zeros((num_of_sets, num_of_vectors, num_of_entries))
    for i in range(num_of_sets):
        idx = rng_idx()
        result[i][0] = data[idx]
        for j in range(1, num_of_vectors):
            sim_values = np.zeros(N)
            def apply_sim(x):
                sim_value = 10.0**9
                for k in range(j):
                    sim_value = min(sim_value, similiarity(result[i][k], x))
            for k in range(N):
                sim_values[k] = apply_sim(data[k])
            sim_values.sort()
            new_vector = data[int(0.2 * N) + random.randint(int(-N/100), int(N/100))]
            result[i][j] = new_vector
        random.shuffle(result[i])


def similiarity(x, y):
    assert len(x) == len(y)
    def relative_error(a, b):
        if a == 0:
            return b
        return (a-b)*(a-b)/(a*a)
    sum = 0
    for i in range(len(x)):
        sum += relative_error(x[i], y[i])
    return sum

def nba_similiarity():
    #result = [[[0]*num_of_entries]*num_of_vectors]*num_of_sets
    for i in range(num_of_sets):
        idx = rng_idx()
        x = data[i]
        result[i][num_of_vectors - 1] = x
        teammates = []
        minutes = []
        for j in range(N):
            if j == idx:
                continue
            y = data[j]
            if x[1] == y[1] and x[0] != y[0]:
                teammates.append(y)
            if abs(x[2] - y[2]) <= 4 and x[0] != y[0]:
                minutes.append(y)
        random.shuffle(teammates)
        random.shuffle(minutes)
        max_team = 2
        for k in range(num_of_vectors - 1):
            if k < max_team:
                result[i][k] = teammates[k] 
            else:
                result[i][k] = minutes[k - max_team]


nba_similiarity()
print(result)



print(similiarity([1, 2, 3], [4, 5, 6]))

np.save(path + name+"_sets.npy", result)



