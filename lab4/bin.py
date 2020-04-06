""""
@Author Filip Twardy
"""
import numpy as np
from vis import plot_anealing
import random

def acceptance_probability(cost, new_cost, temperature):
    if new_cost < cost:
        return 1
    else:
        return np.exp(- (new_cost - cost) / temperature)

def bin_image(dens, n):

    p = int(n*n*dens)
    im = np.zeros((n,n))

    for _ in range(p):
        i = np.random.randint(0, n)
        j = np.random.randint(0, n)

        while im[i][j] == 1:
            i = np.random.randint(0, n)
            j = np.random.randint(0, n)

        im[i][j] = 1

    return im, p
        

def temperature(fraction):
    return max(0.01, min(1, 1 - fraction))

def distance(a, b):
    return np.sqrt((abs(a[0]-b[0]) ** 2 + abs(a[1]-b[1]) ** 2))

def cost_function(im, p, n):
    cost = 0
    for i in range(n):
        for j in range(n):
            if im[i][j] == 1:
                cost += (distance([i, j], [0,0]))

    return cost

def neighbour(im, p):
    n = len(im)

    i = np.random.randint(0, n)
    j = np.random.randint(i, n)

    if im[i][j] == 1:

        for x in range(i):
            if im[x][j] == 0:
                im[i][j], im[x][j] = im[x][j], im[i][j]
                return im

        for x in range(j):
            if im[i][x] == 0:
                im[i][j], im[i][x] = im[i][x], im[i][j]
                return im

    return im

                
def anneal(dens, n, next_state_func, maxsteps=1000):

    state, p = bin_image(dens, n)

    cost = cost_function(state, p, n)

    states, costs = [0], [cost]

    for step in range(1, maxsteps):
        if step % (maxsteps // 10) == 0:
            print(f"Current step {step}")
        fraction = step / float(maxsteps)
        T = temperature(fraction)
        new_state = next_state_func(state, p)
        new_cost = cost_function(new_state, p, n)
        if acceptance_probability(cost, new_cost, T) > random.random():
            state, cost = new_state, new_cost
            states.append(step)
            costs.append(cost)

    return state, cost_function(state, p, n), states, costs
    
if __name__ == "__main__":
    state, cost, states, costs = anneal(0.5, 20, neighbour, maxsteps=1000)

    plot_anealing(states, costs)
