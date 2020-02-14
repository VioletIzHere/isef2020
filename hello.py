
# Intel Science & Engineering Fair Project : 2019-2020
# Code by Paarth Tara

import random
import math

R = 1 # maximum number of individuals eliminated per turn, in any attack strategy
N = 50 # number of time iterations for this simulation
V = 4 # attack strategy: 0 = operations, 1 = propaganda, 2 = recruitment logistics, 3 = central logistics, 4 = all equally
A = 0 # initial number of terrorist attacks (0)
A_op = 4 # number of operations members necessary to conduct one terrorist attack
A_ce = 2 # number of central logistics members necessary to conduct one terrorist attack

class Cell:
    def __init__(self, nodes, destroy_probability):
        self.nodes = nodes
        self.destroy_probability = destroy_probability
    def attack(self):
        nemo = random.randint(1, 100)
        if nemo <= self.destroy_probability:
            if self.nodes >= R:
                self.nodes -= R
    def addToNodes(self, x):
        self.nodes = self.nodes + x

network = [
    Cell(8, 100),  # operations
    Cell(6, 90),   # propaganda
    Cell(6, 70),   # recruitment logistics
    Cell(4, 20)    # central logistics
]

def G(propaganda, recruitment):
    first_part = math.floor(math.pow(1.2, propaganda))
    second_part = math.floor(51 / (1 + math.exp(-0.27 * (recruitment - 15)))) / 100
    return math.ceil(first_part * second_part)

def computeA():
    global A
    a = math.floor(network[0].nodes / A_op)
    b = math.floor(network[3].nodes / A_ce)
    if a <= b:
        for i in range(a):
            j = random.randint(1, 100)
            if j <= 70: A += 1
    else:
        for i in range(b):
            j = random.randint(1, 100)
            if j <= 70: A += 1

data_logger = open("cirrus.csv", "w")
# data_logger.write("t, operations, propaganda, recruitment, central, attacks\n")

def log():
    data_logger.write(str(A) + ",")

for t in [k + 1 for k in list(range(N))]:
    if V != 4:
        gains = G(network[1].nodes, network[2].nodes)
        gains_group1 = math.ceil(gains / 2)
        gains_group2 = gains - gains_group1
        network[V].addToNodes(gains_group1)
        for i in range(gains_group2):
            j = [0, 1, 2, 3]
            k = []
            for l in j:
                if l != V:
                    k.append(l)
            m = random.choice(k)
            network[m].addToNodes(1)
        network[V].attack()
        computeA()
        log()
    else:
        gains = G(network[1].nodes, network[2].nodes)
        for i in range(gains):
            network[random.randint(0, 3)].addToNodes(1)
        network[random.randint(0, 3)].attack()
        computeA()
        log()
    print("COMPUTING ######### " + str(math.floor(t / N * 100)) + "% PROCESSED")

data_logger.close()
