from matplotlib import pyplot as plt
from Constants import *


class Plot:

    def __init__(self, world):

        self.data = {'performedActions': {'wait': [], 'move': [], 'mate': [], 'attack': [], 'changeTeam': []},
                     'teams': {}}

        for team in world.teams:
            self.data['teams'][team] = {'population': [],
                                        'genAverage': {'wait': [], 'move': [], 'mate': [],
                                                       'attack': [], 'changeTeam': []}}

        self.x = []
        # self.figure, self.axes = plt.subplots(3)
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(111)
        self.plotInitialized = False
        self.populationPlots = {team: None for team in world.teams}
        self.axes.set_ylim([0, 1.5 * (world.width * world.height) * (neighbourLimit / 8) / nTeams])
        self.axes.set_xlabel('Epoch')
        self.axes.set_ylabel('Population')


    def update(self, world):

        self.x.append(world.epoch)
        self.axes.set_xlim([0, world.epoch])

        for action in self.data['performedActions']:
            self.data['performedActions'][action].append(world.performedActions[action])

        for team in self.data['teams']:
            self.data['teams'][team]['population'].append(0)
            for gen in self.data['teams'][team]['genAverage']:
                self.data['teams'][team]['genAverage'][gen].append(0)

        for cell in world.cells:
            self.data['teams'][cell.team]['population'][-1] += 1
            for gen in cell.genes:
                self.data['teams'][cell.team]['genAverage'][gen][-1] += cell.genes[gen]

        for team in self.data['teams']:
            teamPopulation = self.data['teams'][team]['population'][-1]
            for gen in self.data['teams'][team]['genAverage']:
                self.data['teams'][team]['genAverage'][gen][-1] /= teamPopulation

        # Plot
        if not self.plotInitialized:
            self.plotInitialized = True
            for team in world.teams:
                color = [i / 255 for i in colors[team]]
                color.append(1) # alpha
                self.populationPlots[team], = self.axes.plot(self.x, self.data['teams'][team]['population'], color=color)
            # self.actionPlot = self.axes[1].plot(self.x)
            # self.genPlot = self.axes[2].plot(self.x)

            plt.ion()   # interactive mode
            plt.show()

        else:

            for team in world.teams:
                if self.axes.get_ylim()[1] < self.data['teams'][team]['population'][-1]:
                    self.axes.set_ylim([0, 1.2 * self.axes.get_ylim()[1]])

                self.populationPlots[team].set_xdata(self.x)
                self.populationPlots[team].set_ydata(self.data['teams'][team]['population'])

            plt.pause(0.001)