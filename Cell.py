import random
from Constants import *


class Cell:

    maxAge = cellMaxAge
    maxLifePoints = cellMaxLifePoints

    def __init__(self, team, row, col, parents=None):
        self.team = team
        self.row = row
        self.col = col
        self.age = 0
        self.genes = {'wait': 0.0, 'move': 0.0, 'mate': 0.0, 'attack': 0.0, 'changeTeam': 0.0}
        self.lifePoints = random.uniform(cellMinStartingLifeFactor * self.maxLifePoints, self.maxLifePoints)

        weight = 0.0

        if not parents:
            for gen in self.genes:
                self.genes[gen] = random.random() * geneticMask[self.team][gen]
                weight += self.genes[gen]
        else:
            if random.random() > cellMutationRate:
                for gen in self.genes:
                    self.genes[gen] = sum([p.genes[gen] for p in parents]) / len(parents)
                    weight += self.genes[gen]

            # Mutation
            else:
                for gen in self.genes:
                    self.genes[gen] = random.random()
                    weight += self.genes[gen]

        # Gen normalization
        for gen in self.genes:
            self.genes[gen] /= weight


    def isAlive(self):
        return self.lifePoints > 0 and self.age <= self.maxAge


    def normalizePosition(self, worldWidth, worldHeight):
        self.row = self.row % worldHeight
        self.col = self.col % worldWidth


    def selectAction(self, environment):
        self.age += 1
        actionSet = {'wait': 1,
                     'move': environment.count('empty'),
                     'mate': environment.count('friend') if environment.count('empty') > 0 else 0, # Mating also needs empty space
                     'attack': environment.count('foe'),
                     'changeTeam': environment.count('foe')}

        # Action normalization
        actionWeight = 0
        for action in actionSet:
            actionWeight += actionSet[action]
        for action in actionSet:
            actionSet[action] /= actionWeight

        # Combine genetic weight and environmental weight and select action
        combinedWeights=[self.genes[action] * actionSet[action] for action in actionSet]
        action = random.choices(list(actionSet.keys()), weights=combinedWeights, k=1)[0]

        # Select target
        targetPositions = []
        spawnPositions = []

        if action == 'wait':
            targetPositions.append(4) # 4 is the center of the environment, self
                                      # 0 1 2
                                      # 3 4 5
                                      # 6 7 8
        elif action == 'move':
            for i in range(len(environment)):
                if environment[i] == 'empty':
                    targetPositions.append(i)

        elif action == 'mate':
            for i in range(len(environment)):
                if environment[i] == 'friend':
                    targetPositions.append(i)

            for i in range(len(environment)):
                if environment[i] == 'empty':
                    spawnPositions.append(i)

        elif action in ['attack', 'changeTeam']:
            for i in range(len(environment)):
                if environment[i] == 'foe':
                    targetPositions.append(i)

        targetPosition = random.choice(targetPositions)
        targetPositionDelta = (int(targetPosition / 3) - 1, targetPosition % 3 - 1)

        spawnPosition = random.choice(spawnPositions) if len(spawnPositions) > 0 else None
        spawnPositionDelta = (int(spawnPosition / 3) - 1, spawnPosition % 3 - 1) if spawnPosition != None else None

        return action, targetPositionDelta, spawnPositionDelta