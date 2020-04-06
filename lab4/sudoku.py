"""
@author Filip Twardy
"""
import numpy as np
import random
from vis import plot_anealing

def temperature(fraction):
    return max(0.01, min(1, 1 - fraction))

def acceptance_probability(cost, new_cost, temperature):
    if new_cost < cost:
        return 1
    else:
        return np.exp(- (new_cost - cost) / temperature)

def load_sudoku(foo):

    sudoku = np.zeros((9,9))
    game = np.zeros((9,9))
    i = 0

    with open(foo) as f:
        lines = f.readlines()
        
        for line in lines:
            for idx, sign in enumerate(line):
                if sign != '0' and sign != '\n':
                    sudoku[i][idx] = 1
                    game[i][idx] = int(sign)
            i += 1

    return sudoku, game

def cost_function(game):

    cost = 0
    for row in game:
        S = set()
        for e in row:
            if e != 0:
                S.add(e)
        cost += len(S)

    for col in game.T:
        S = set()
        for e in col:
            if e != 0:
                S.add(e)
        cost += len(S)

    for x in range(3):
        for y in range(3):
            cube = game[x*3:x*3+3, y*3:y*3+3]
            S = set()
            for e in cube.flatten():
                if e != 0:
                    S.add(e)
            cost += len(S)

    return 81*3 - cost

def neighbour(game, sudoku):

    for idx, row in enumerate(game):
        nums = [1,2,3,4,5,6,7,8,9]
        if not check(row):
            nums = list(set(nums) - set(row[sudoku[idx] == 1]))
            row[sudoku[idx] == 0] = np.random.permutation(nums)

    for idx, row in enumerate(game.T):
        nums = [1,2,3,4,5,6,7,8,9]
        if not check(row):
            nums = list(set(nums) - set(row[sudoku.T[idx] == 1]))
            row[sudoku.T[idx] == 0] = np.random.permutation(nums)

    return game

def init_game(game, sudoku):
    game[sudoku == 0] = np.random.randint(1, 10, (9,9))[sudoku == 0]
    return game

def check(row):
    s = set()
    for e in row:
        if e != 0:
            s.add(e)
    return len(s) == 9


def anneal(game, sudoku, maxsteps=1000):

    state = init_game(game, sudoku)

    cost = cost_function(state)

    states, costs = [0], [cost]

    for step in range(1, maxsteps):
        if step % (maxsteps // 10) == 0:
            print(f"Current step {step}")
        fraction = step / float(maxsteps)
        T = temperature(fraction)
        new_state = neighbour(state, sudoku)
        new_cost = cost_function(new_state)
        if acceptance_probability(cost, new_cost, T) > random.random():
            state, cost = new_state, new_cost
            states.append(step)
            costs.append(cost)

    return state, cost_function(state), states, costs
    
if __name__ == "__main__":
    sudoku, game = load_sudoku("sudoku.txt")
    state, cost, states, costs = anneal(game, sudoku, maxsteps=50000)
    print(cost)
    print(state)
    plot_anealing(states, costs)

