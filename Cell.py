import random
from Constants import *


class Cell:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.infected = -1
        self.alive = True
        self.passedIt = False


    def isAlive(self):
        return self.alive


    def isInfected(self):
        return self.infected != -1


    def selectAction(self, environment, epoch, infectedPercentage):

        # Infection
        if not self.isInfected() and not self.passedIt:
            infectedNeighbours = environment.count('infected')
            infProb = 1 - (1 - infectionProbability) ** infectedNeighbours
            if random.random() < infProb:
                self.infected = epoch

        # Death
        deathProb = deathProbability
        if infectedPercentage > systemCapacity:
            deathProb = deathProbability * (infectedPercentage/systemCapacity) * 10
        if self.isInfected() and random.random() < deathProb:
            self.alive = False

        # Curation
        if self.isInfected() and (epoch - self.infected) >= epochsToCure:
            self.infected = -1
            self.passedIt = True

        action = random.choices(['wait', 'move'], weights=[1 - moveProb, moveProb], k=1)[0]

        # Select target
        targetPositions = []

        if action == 'wait':
            targetPositions.append(4) # 4 is the center of the environment, self
                                      # 0 1 2
                                      # 3 4 5
                                      # 6 7 8
        elif action == 'move':
            for i in range(len(environment)):
                if environment[i] == 'empty':
                    targetPositions.append(i)


        targetPosition = random.choice(targetPositions)
        targetPositionDelta = (int(targetPosition / 3) - 1, targetPosition % 3 - 1)

        return action, targetPositionDelta