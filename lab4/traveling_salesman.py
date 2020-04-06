"""
@Author Filip Twardy
"""
import math
import numpy as np
from numpy import random
from vis import plot_anealing
from itertools import product
import random as r


def acceptance_probability(cost, new_cost, temperature):
    if new_cost < cost:
        return 1
    else:
        return np.exp(- (new_cost - cost) / temperature)

def consectutive_swap(cities):
    i = random.randint(0, len(cities) - 2)
    cities[i], cities[i+1] = cities[i+1], cities[i]
    return cities

def arbitary_swap(cities):
    l = random.randint(2, len(cities) - 1)
    i = random.randint(0, len(cities) - l)
    cities[i], cities[i+l] = cities[i+l], cities[i]
    return cities

def cost_function(path, dist_matrix):
    cost = 0
    for i in range(len(path)-1):
        cost += dist_matrix[path[i][1]][path[i+1][1]]

    return cost

def distance(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def calculate_dist_matrix(states):

    dist_matrix = np.zeros((len(states), len(states)))

    for x  in states:
        for y in states:
            u, u_idx = x 
            v, v_idx = y
            dist = distance(u, v)
            dist_matrix[u_idx][v_idx] = dist
            dist_matrix[v_idx][u_idx] = dist
        
    return dist_matrix 

def basic_example():
    cities = [([1,0], 1),
              ([0,0], 0),
              ([1,1], 2),
              ([0,1], 3)]

    return cities 


def anneal(random_start, next_state_func, maxsteps=1000):

    state = random_start()

    dist_matrix = calculate_dist_matrix(state)

    cost = cost_function(state, dist_matrix)

    states, costs = [0], [cost]
    
    T = 1000

    for step in range(1, maxsteps):
        if step % (maxsteps // 10) == 0:
            print(f"Current step {step}")
        fraction = step / float(maxsteps)
        T *= 0.99
        new_state = next_state_func(state)
        new_cost = cost_function(new_state, dist_matrix)
        if acceptance_probability(cost, new_cost, T) > random.uniform(0, 1):
            state, cost = new_state, new_cost
            states.append(step)
            costs.append(cost)
        

    return state, cost_function(state, dist_matrix), states, costs


if __name__ == "__main__":
    state, cost, states, costs = anneal(basic_example, consectutive_swap, maxsteps=10)
    plot_anealing(states, costs)

