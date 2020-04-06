import numpy as np

def uniform_distro(low, high, n):
    return [[x, idx]
            for idx, x in
            enumerate(np.random.uniform(low, high, (n, 2)))]

def normal_distro(mu, sigma, n):
    return [[x, idx]
            for idx, x in
            enumerate(np.random.normal(mu, sigma, (n, 2)))]


def nine_groups(low, high, n):	
    return [uniform_distro(low/18*i, high/18*(i+1), int(n/9)) for i in range(0, 18, 2)]


