# from random import randint
from BaseAI import BaseAI
import sys
import math
import time

class PlayerAI(BaseAI):
    infty = 1e10
    startTime = 0.0
    maxdepth = 0

    def getMove(self, grid):
        self.startTime = time.time()
        self.maxdepth = 0
        if grid.getAvailableMoves():
            direction, _ = self.maximize(grid, 0)
            print(self.maxdepth)
            return direction
        else:
            return 1

    def maximize(self, grid, depth):
        # if depth == 4 or not grid.getAvailableMoves(dirs=[0,2,3,1]):
        if depth > self.maxdepth:
            self.maxdepth = depth
        if time.time() - self.startTime > 0.05 or not grid.getAvailableMoves(dirs=[0,2,3,1])\
                or depth > 10:
            return None, self.utility(grid)
        max_util = -self.infty
        max_dir = None
        moves = grid.getAvailableMoves(dirs=[0,2,3,1])
        if len(moves) > 1:
            for i in moves:
                g = grid.clone()
                g.move(i)
                _, utility = self.minimize(g, depth+1)
                # if i == 1:
                    # utility *= 0.98
                if depth == 0:
                    print("Max at ", i, utility)
                if utility > max_util:
                    max_util = utility
                    max_dir = i
        else:
            max_dir = moves[0]
            max_util = self.utility(grid)
        # print("Max", max_dir)
        return (max_dir, max_util)

    def minimize(self, grid, depth):
        # print(depth)
        if depth > self.maxdepth:
            self.maxdepth = depth
        if time.time() - self.startTime > 0.05 or not grid.getAvailableMoves(dirs=[0,2,3,1])\
                or depth > 10:
            # print(time.time() - self.startTime)
            return None, self.utility(grid)
        min_util = self.infty
        min_child = None
        # print("depth = ", depth)
        # print("Min")
        for cell in grid.getAvailableCells():
            for val in [2]:
                g = grid.clone()
                g.setCellValue(cell, val)
                _, utility = self.maximize(g, depth+1)
                # if depth == 1:
                #     print("Min at ", depth, utility)
                if utility < min_util:
                    min_util = utility
                    min_child = g
        return (min_child, min_util)

    def utility(self, grid):
        m = []
        for el in grid.map:
            m.extend([val for val in el])
        m = sorted(m, reverse=True)
        nonzero = [val for val in m if val > 0]
        # print("m")
        # print(sum(m)/len(m))
        # return 2
        # maxtile = grid.getMaxTile()
        posmax = (0,0)
        posmax1 = (0,0)
        num = 0
        for i, row in enumerate(grid.map):
            for j, val in enumerate(row):
                if j != 3 and row[j] == row[j+1]:
                    num += 1
                if val == m[0]:
                    posmax = (i, j)
                if val == m[1] and m[1]>0:
                    posmax1 = (i, j)

        # print(grid.map)
        mon, merg = self.monotonicity(grid)
        # print(merg)
        # sys.exit(0)
        return len(grid.getAvailableCells())+\
                mon/3 + merg/2
                # (int(posmax==(0,0))+int(posmax==(0,3))+
                # int(posmax==(3,0))+int(posmax==(3,3))) +\
                # 0.1*math.log(sum(nonzero)/len(nonzero),2) +\
                # 0.1*math.log(max(nonzero),2)
                # num/10+\
                # 0.5*int(abs(posmax[0]-posmax1[0]+posmax[1]-posmax1[1]) == 1)+\
        # return len(grid.getAvailableCells())+0.3*sum([math.log(val,2) for val in m[:3] if val > 0])+\
        #         max(m)
    def monotonicity(self, grid):
        total = [0,0,0,0]
        mergable = 0
        # left/right
        for row in grid.map:
            current = 0
            nex = current + 1
            while nex<4:
                while row[nex] == 0 and nex < 3:
                    nex += 1
                if row[current] > row[nex]:
                    total[0] += 1
                    if row[current] == 2*row[nex]:
                        total[0] += 1
                elif row[current] < row[nex]:
                    total[1] += 1
                    if 2*row[current] == row[nex]:
                        total[0] += 1
                if row[current] > 0 and row[current] == row[nex]:
                    mergable += 1
                # print(row[current], row[nex])
                current = nex
                nex += 1
        # up/down
        for j in range(4):
            current = 0
            nex = current + 1
            while nex<4:
                while grid.map[nex][j] == 0 and nex < 3:
                    nex += 1
                if grid.map[current][j] > grid.map[nex][j]:
                    total[2] += 1
                    if grid.map[current][j] == 2*grid.map[nex][j]:
                        total[2] += 1
                elif grid.map[current][j] < grid.map[nex][j]:
                    total[3] += 1
                    if 2*grid.map[current][j] == grid.map[nex][j]:
                        total[3] += 1
                if grid.map[current][j] > 0 and grid.map[current][j] == grid.map[nex][j]:
                    mergable += 1
                # print(row[current], row[nex])
                current = nex
                nex += 1
        return max(total[0],total[1]) + max(total[2],total[3]), mergable

            