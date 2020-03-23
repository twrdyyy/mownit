import networkx as nx
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import lu
from time import time

sys.setrecursionlimit(10**8)

def gauss_jordan(A):

    B = A.copy()
    start = time()
    for idx in range(len(A)):
        pivot = A[idx][idx]
        for row in range(len(A)):
            if row != idx:
                to_zero = A[row][idx]
                for el in range(len(A[row])):
                    A[row][el] -= A[idx][el] / pivot * to_zero
    Ans = [A[x][-1] / A[x][x] for x in range(len(A))]
    stop = time()
    print(f"GAUSS time: {stop - start}")
    start = time()
    B = np.linalg.solve(B[:, :-1], B[:, -1])
    stop = time()
    print(f"NUMPY time: {stop - start}")


def lu_factorization(A):

    B = A.copy()
    #normalization
    B = B / np.max(B)
    start = time()
    P = [[float(x == y) for x in range(len(A))] for y in range(len(A))]
    for i in range(len(P)):
        row = max(range(i, len(P)), key=lambda x: abs(B[x][i]))
        if i != row:
            P[i], P[row] = P[row], P[i]

    PA = B @ P
    L = np.zeros(A.shape, dtype=np.float64)
    U = np.zeros(A.shape, dtype=np.float64)

    for i in range(len(A)):
        L[i][i] = 1.0

        for j in range(i+1):
            U[j][i] = PA[j][i] - np.sum([U[x][i] * L[j][x] for x in range(j)])

        for j in range(i+1, len(A)):
            L[j][i] = (PA[j][i] - np.sum([U[x][i] * L[j][x] for x in range(i)])) / U[i][i]
    stop = time()

    print(f"OWN IMPLEMENTATION time = {stop - start}")
    start = time()
    P_, L_, U_ = lu(B)
    stop = time()
    print(f"SCIPY IMPLEMENTATION time = {stop - start}")

def loadWeightedGraph(name):
    V = 0
    L = []

    with open(name) as f:
        lines = f.readlines()
        for line in lines:
            s = line.split(" ")
            if len(s) < 1:
                continue
            elif s[0] == "p":
                V = int(s[2])
            elif s[0] == "e":
                (a, b, c) = (int(s[1]), int(s[2]), float(s[3]))
                L.append((min(a,b), max(a,b), c))
    return (V, L)

def set_I(curr, N, I, L, visited, s, t):

    if visited[curr]:
        return
    visited[curr] = True
    q = curr

    for node in N[curr].keys():
        if curr == t and node == s:
            continue
        tmp = L[(min(curr, node), max(curr, node))][0]
        if I[q][tmp] == 0:
            I[q][tmp] = -1
        if I[node][tmp] == 0:
            I[node][tmp] = 1
        set_I(node, N, I, L, visited, s, t)


def dfs(N, start, end):
    f = [(start, [])]
    while f:
        state, path = f.pop()
        if path and state == end:
            yield path
            continue
        for next_state in N[state].keys():
            if next_state in path:
                continue
            f.append((next_state, path+[next_state]))

def get_cycle(N):
    cycles = set([tuple([node] + path) for node in range(1, len(N)) \
                                       for path in dfs(N, node, node) \
                                       if len(path) != 2])
    cycles = [x for x in cycles if len(x) -1 == len(set(x))]
    return cycles

def wire_analysis(name, s, t, E):
    V, L = loadWeightedGraph(name)

    N = [{} for _ in range(V+1)]
    for x, y, c in L:
        N[x][y] = c
        N[y][x] = c

    L = {(min(x[0], x[1]), max(x[0], x[1])) : (idx+1, x[2]) for idx, x in enumerate(L)}

    I = np.zeros((len(L) + 1, len(L) + 1))
    I_ANS = [0 for _ in range(V)]

    visited = [False for _ in range(V+1)]
    set_I(s, N, I, L, visited, s, t)

    cycles = get_cycle(N)
    for key, val in L.items():
        x, y = key
        idx, c = val
        N[x][y] = c*I[x][idx]
        N[y][x] = c*I[y][idx]

    curr_q = V+1

    for cycle_idx in range(len(cycles)):
        cycle = cycles[cycle_idx]
        if s in cycle and t in cycle:
            for idx in range(len(cycle)-1):
                i, c = L[(min(cycle[idx], cycle[idx+1]), max(cycle[idx], cycle[idx+1]))]
                I[curr_q][i] = c
            cycles[cycle_idx] = []
            break
    I_ANS.append(-1*E)
    curr_q += 1

    while curr_q <= len(L):
        for cycle_idx in range(len(cycles)):
            cycle = cycles[cycle_idx]
            if len(cycle) == 0:
                continue
            for idx in range(len(cycle)-1):
                i, c = L[(min(cycle[idx], cycle[idx+1]), max(cycle[idx], cycle[idx+1]))]
                I[curr_q][i] = c
            cycles[cycle_idx] = []
            break
        curr_q += 1
        I_ANS.append(0)

    I = np.array(I)[1:, 1:]
    SOL = np.linalg.solve(I,I_ANS)

    S = "'p edge " + str(V) + " " + str(len(L)) 
    for key, val in L.items():
        S += "\n"
        x, y = key
        idx, _ = val
        S += f"e {x} {y} {SOL[idx-1]}"

    S += "'"
    os.system("echo " + S + " >> sol.txt")

def main():
    test = [(1, 10, 100), (1, 100, 50), (1, 5, 10)]
    for low, high, size in test:
        print("1exe")
        gauss_jordan(np.random.uniform(low, high, (size,size+1)))
        print("2exe")

        lu_factorization(np.random.uniform(low, high, (size, size)))

    wire_analysis("clique5", 1, 2, 100)
    pass


if __name__ == '__main__':
    main()
