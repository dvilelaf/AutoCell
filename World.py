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
        self.epoch = 0
        self.data = {'healthy': initialPopulation - nPatientZero, 'infected': nPatientZero, 'deaths': 0, 'inmune': 0}
        self.population = initialPopulation

        while len(self.cells) < self.initialPopulation:
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            if self.empty(row, col):
                self.cells.append(Cell(row, col))
                self.set(row, col, self.cells[-1]) # Map is synced with cells and shares objects

        for i in range(nPatientZero):
            self.cells[i].infected = 0


    def get(self, row, col):
        return self.map[row % self.height][col % self.width]


    def set(self, row, col, newValue):
        self.map[row % self.height][col % self.width] = newValue


    def empty(self, row, col):
        return self.get(row, col) == None


    def kill(self, index):
        cell = self.cells[index]
        self.set(cell.row, cell.col, None)
        del self.cells[index]


    def step(self):
        # Use an independent list to avoid modifying inside a loop
        cellIndexList = list(range(len(self.cells)))
        # Ensure random decision order
        random.shuffle(cellIndexList)

        for cellIndex in cellIndexList:
            cell = self.cells[cellIndex]

            if cell.isAlive(): # Some cells may have been killed by a neighbour

                emptyNeighbours = 0
                friendNeighbours = 0
                foeNeighbours = 0
                environment = []

                # Environment
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
                                if neighbour.isInfected():
                                    environment.append('infected')
                                else:
                                    environment.append('healthy')

                # Action selection
                action, targetPositionDelta = cell.selectAction(environment, self.epoch, 100 * self.data['infected'] / startingPopulation)

                targetPosition = ((cell.row + targetPositionDelta[0]) % self.height, (cell.col + targetPositionDelta[1]) % self.width)

                if action == 'wait':
                    pass

                elif action == 'move':
                    cell.row = targetPosition[0]
                    cell.col = targetPosition[1]


        # Clean dead cells
        deletionList = []
        for i in range(len(self.cells)):
            if not self.cells[i].isAlive():
                deletionList.append(i)

        for i in sorted(deletionList, reverse=True):
            self.kill(i)

        # Increase epoch
        self.epoch += 1

        self.data['deaths'] = len(deletionList)
        self.data['healthy'] = 0
        self.data['infected'] = 0
        self.data['inmune'] = 0

        for cell in self.cells:
            if cell.infected > -1:
                self.data['infected'] += 1
            else:
                self.data['healthy'] += 1
                if cell.passedIt:
                    self.data['inmune'] += 1

        self.population = self.data['healthy'] + self.data['infected']

        print(f"Epoch {self.epoch:>5}    cells: {len(self.cells):>5}    healthy: {self.data['healthy']:>5}    infected: {self.data['infected']:>5}    deaths: {self.data['deaths']:>5}")