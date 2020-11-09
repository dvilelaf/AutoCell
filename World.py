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
        self.actions = {team: {'wait': 0, 'move': 0, 'mate': 0, 'attack': 0, 'changeTeam': 0, 'none': 0} for team in self.teams}

        while len(self.cells) < self.initialPopulation:
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            team = random.choice(self.teams)
            if self.empty(row, col):
                self.cells.append(Cell(team, row, col))
                self.set(row, col, self.cells[-1]) # Map is synced with cells and shares objects
                self.populations[team] += 1


    def get(self, row, col):
        return self.map[row % self.height][col % self.width]


    def set(self, row, col, newValue):
        self.map[row % self.height][col % self.width] = newValue


    def empty(self, row, col):
        return self.get(row, col) == None


    def spawn(self, row, col, parents):
        team = parents[0].team
        self.cells.append(Cell(team, row, col, parents=parents))
        self.set(row, col, self.cells[-1]) # Keep map synced
        self.populations[team] += 1


    def kill(self, index):
        cell = self.cells[index]
        self.populations[cell.team] -= 1
        self.set(cell.row, cell.col, None) # Keep map synced
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
                                if neighbour.team == cell.team:
                                    friendNeighbours += 1
                                    environment.append('friend')
                                else:
                                    foeNeighbours += 1
                                    environment.append('foe')

                # Death by overpopulation
                if (friendNeighbours + foeNeighbours) > neighbourLimit:
                    cell.lifePoints = 0
                    continue

                # Action selection
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

                elif action == 'mate':
                    cell.lifePoints -= cellMatingFactor
                    self.spawn(spawnPosition[0], spawnPosition[1], parents=(cell, target))

                elif action == 'attack':
                    lifeDelta = min((target.lifePoints, cell.lifePoints))
                    cell.lifePoints -= lifeDelta
                    target.lifePoints -= lifeDelta

                elif action == 'changeTeam':
                    self.populations[cell.team] -= 1
                    self.populations[target.team] += 1
                    cell.team = target.team

        # Clean dead cells
        deletionList = []
        for i in range(len(self.cells)):
            if not self.cells[i].isAlive():
                deletionList.append(i)

        for i in sorted(deletionList, reverse=True):
            self.kill(i)

        # Increase epoch
        self.epoch += 1

        # Count actions of living cells
        self.actions = {team: {'wait': 0, 'move': 0, 'mate': 0, 'attack': 0, 'changeTeam': 0, 'none': 0} for team in self.teams}
        totalActions = {'wait': 0, 'move': 0, 'mate': 0, 'attack': 0, 'changeTeam': 0, 'none': 0}

        for cell in self.cells:
            self.actions[cell.team][cell.lastAction] += 1
            totalActions[cell.lastAction] += 1

        if logData:
            print(f"Epoch {self.epoch:>5}    cells: {len(self.cells):>5}    "
                  f"waits: {totalActions['wait']:>5}    moves: {totalActions['move']:>5}    "
                  f"mates: {totalActions['mate']:>5}  attacks: {totalActions['attack']:>5}    "
                  f"changeTeams: {totalActions['changeTeam']:>4}    none: {totalActions['none']:>5}")