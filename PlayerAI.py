from random import randint
from BaseAI import BaseAI


class PlayerAI(BaseAI):
    def getMove(self, grid):
        return randint(0, 3)