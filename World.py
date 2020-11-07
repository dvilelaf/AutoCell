from Cell import Cell
import random
from Constants import *


class World:

    def __init__(self, width=25, height=25, population=None, nTeams=2):
        self.width = width
        self.height = height
        self.map = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.population = population if population else width
        self.cells = []
        self.teams = []
        self.epoch = 0

        for color in colors:
            self.teams.append(color)
            if len(self.teams) == nTeams:
                break

        while len(self.cells) < self.population:
            row = random.randint(0, self.width - 1)
            col = random.randint(0, self.height - 1)
            team = random.choice(self.teams)
            if self.empty(row, col):
                self.cells.append(Cell(team, row, col))
                self.set(row, col, self.cells[-1]) # Map is synced with cells and shares objects


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

        performedActions = {'wait': 0, 'move': 0, 'mate': 0, 'attack': 0, 'changeTeam': 0}

        for cellIndex in cellIndexList:
            cell = self.cells[cellIndex]

            if cell.isAlive():

                emptyNeighbours = 0
                friendNeighbours = 0
                foesNeighbours = 0
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
                                    foesNeighbours += 1
                                    environment.append('foe')

                action, targetPositionDelta, spawnPositionDelta = cell.selectAction(environment)

                targetPosition = ((cell.row + targetPositionDelta[0]) % self.height, (cell.col + targetPositionDelta[1]) % self.width)
                target = self.get(targetPosition[0], targetPosition[1])

                spawnPosition = ((cell.row + spawnPositionDelta[0]) % self.height, (cell.col + spawnPositionDelta[1]) % self.width) if spawnPositionDelta else None

                performedActions[action] += 1

                if action == 'wait':
                    pass

                elif action == 'move':
                    cell.row = targetPosition[0]
                    cell.col = targetPosition[1]
                    cell.normalizePosition(self.width, self.height)

                elif action == 'mate':
                    cell.lifePoints = int((1 - cellMatingFactor) * cell.lifePoints)
                    self.cells.append(Cell(cell.team, spawnPosition[0], spawnPosition[1], parents=(cell, target)))
                    self.set(targetPosition[0], targetPosition[1], self.cells[-1]) # Keep map synced

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
            self.cells[i] = None # Keep map synced
            del self.cells[i]

        print(f"Epoch {self.epoch}  cells: {len(self.cells)}  waits: {performedActions['wait']}  moves: {performedActions['move']}  mates: {performedActions['mate']}  attacks: {performedActions['attack']}  changeTeams: {performedActions['changeTeam']}")

        self.epoch += 1