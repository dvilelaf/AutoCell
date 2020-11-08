from Cell import Cell
import random
from Constants import *


class World:

    def __init__(self, width=25, height=25, initialPopulation=None, nTeams=2):
        self.width = width
        self.height = height
        self.map = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.initialPopulation = initialPopulation if initialPopulation else width
        self.cells = []
        self.teams = []
        self.epoch = -1

        for color in colors:
            self.teams.append(color)
            if len(self.teams) == nTeams:
                break

        self.populations = {team: 0 for team in self.teams}

        while len(self.cells) < self.initialPopulation:
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            team = random.choice(self.teams)
            if self.empty(row, col):
                self.cells.append(Cell(team, row, col))
                self.set(row, col, self.cells[-1]) # Map is synced with cells and shares objects
                self.populations[team] += 1


        # Genetic mask normalization
        for team in geneticMask:
            weight = 0.0
            for genWeight in geneticMask[team].values():
                weight += genWeight
            for gen in geneticMask[team].keys():
                geneticMask[team][gen] /= weight


    def get(self, row, col):
        return self.map[row % self.height][col % self.width]


    def set(self, row, col, newValue):
        self.map[row % self.height][col % self.width] = newValue


    def empty(self, row, col):
        return self.get(row, col) == None


    def step(self):
        # Use an independent list to avoid modifying inside a loop
        cellIndexList = list(range(len(self.cells)))
        # Ensure random decision order
        random.shuffle(cellIndexList)

        self.actions = {team: {'wait': 0, 'move': 0, 'mate': 0, 'attack': 0, 'changeTeam': 0} for team in self.teams}

        for cellIndex in cellIndexList:
            cell = self.cells[cellIndex]

            if cell.isAlive():

                emptyNeighbours = 0
                friendNeighbours = 0
                foeNeighbours = 0
                environment = []

                for rowDelta in [-1, 0, 1]:
                    for colDelta in [-1, 0, 1]:
                        if (rowDelta == 0 and colDelta == 0): # Skip self position
                             environment.append('me')
                        else:
                            neighbour = self.get(cell.row + rowDelta, cell.col + colDelta)
                            if neighbour == None or not neighbour.isAlive():
                                emptyNeighbours += 1
                                environment.append('empty')
                            else:
                                if neighbour.team == cell.team:
                                    friendNeighbours += 1
                                    environment.append('friend')
                                else:
                                    foeNeighbours += 1
                                    environment.append('foe')

                if (friendNeighbours + foeNeighbours) > neighbourLimit:
                    cell.lifePoints = 0
                    continue

                action, targetPositionDelta, spawnPositionDelta = cell.selectAction(environment)

                targetPosition = ((cell.row + targetPositionDelta[0]) % self.height, (cell.col + targetPositionDelta[1]) % self.width)
                target = self.get(targetPosition[0], targetPosition[1])

                spawnPosition = ((cell.row + spawnPositionDelta[0]) % self.height, (cell.col + spawnPositionDelta[1]) % self.width) if spawnPositionDelta else None

                self.actions[cell.team][action] += 1

                if action == 'wait':
                    pass

                elif action == 'move':
                    cell.row = targetPosition[0]
                    cell.col = targetPosition[1]
                    cell.normalizePosition(self.width, self.height)

                elif action == 'mate':
                    cell.lifePoints = int((1 - cellMatingFactor) * cell.lifePoints)
                    self.cells.append(Cell(cell.team, spawnPosition[0], spawnPosition[1], parents=(cell, target)))
                    self.set(spawnPosition[0], spawnPosition[1], self.cells[-1]) # Keep map synced
                    self.populations[cell.team] += 1

                elif action == 'attack':
                    lifeDelta = min((target.lifePoints, cell.lifePoints))
                    cell.lifePoints -= lifeDelta
                    target.lifePoints -= lifeDelta

                elif action == 'changeTeam':
                    cell.team = target.team


        # Clean dead cells
        deletionList = []
        for i in range(len(self.cells)):
            if not self.cells[i].isAlive():
                deletionList.append(i)

        for i in sorted(deletionList, reverse=True):
            self.populations[self.cells[i].team] -= 1
            self.cells[i] = None # Keep map synced
            del self.cells[i]

        self.epoch += 1

        if logData:

            totalActions = {'wait': 0, 'move': 0, 'mate': 0, 'attack': 0, 'changeTeam': 0}
            for action in totalActions:
                for team in self.teams:
                    totalActions[action] += self.actions[team][action]

            print("Epoch {}  cells: {}  waits: {}  moves: {}  mates: {}  attacks: {}  changeTeams: {}"
                  .format(self.epoch, len(self.cells),
                          totalActions['wait'],
                          totalActions['move'],
                          totalActions['mate'],
                          totalActions['attack'],
                          totalActions['changeTeam']))