from matplotlib import pyplot as plt
from Constants import *
from matplotlib.gridspec import GridSpec


class Plot:

    genes = ('wait', 'move', 'mate', 'attack', 'changeTeam')

    def __init__(self, world):

        # Init data
        self.data = {team: {}  for team in world.teams}
        for team in world.teams:
            self.data[team] = {'population': [],
                               'genes': {action: [] for action in self.genes},
                               'actions': {action: [] for action in self.genes}}
        self.x = []

        # Figure and grid
        self.plotInitialized = False
        self.figure = plt.figure(constrained_layout=True)
        gs = GridSpec(5, 3, figure=self.figure)

        # Init axes
        self.axes = {'population': self.figure.add_subplot(gs[:, 0]),
                     'genes': {action: None for action in self.genes},
                     'actions': {action: None for action in self.genes}}
        i = 0
        for gen in self.genes:
            self.axes['genes'][gen] = self.figure.add_subplot(gs[i, 1])
            i += 1

        i = 0
        for gen in self.genes:
            self.axes['actions'][gen] = self.figure.add_subplot(gs[i, 2])
            i += 1

        # Plots
        self.plots = {'population': {team: None for team in world.teams},
                      'genes': {action: {team: None for team in world.teams} for action in self.genes},
                      'actions': {action: {team: None for team in world.teams} for action in self.genes}}

        # Set axes labels and limits
        maxPopulationGuess = 1.5 * (world.width * world.height) * (neighbourLimit / 8) / nTeams

        self.axes['population'].set_ylim([0, maxPopulationGuess])
        self.axes['population'].set_title('Population')

        for gen in self.axes['genes']:
            self.axes['genes'][gen].set_ylim([0, 1])
            self.axes['genes'][gen].set_ylabel(gen)

            self.axes['actions'][gen].set_ylim([0, 1])
            self.axes['actions'][gen].set_ylabel(gen)

        self.axes['genes']['wait'].set_title('Gen average')
        self.axes['actions']['wait'].set_title('Action average')


    def update(self, world):

        # Update data
        self.x.append(world.epoch)

        for team in world.teams:
            self.data[team]['population'].append(world.populations[team]) # Add populations

            for gen in self.genes:
                self.data[team]['genes'][gen].append(0) # Init gen average

        for cell in world.cells:
            for gen in cell.genes:
                self.data[cell.team]['genes'][gen][-1] += cell.genes[gen] # Add gen values

        for team in world.teams:
            for gen in self.genes:
                if world.populations[team] > 0:
                    self.data[team]['genes'][gen][-1] /= world.populations[team] # Average genes
                    self.data[team]['actions'][gen].append(world.actions[team][gen] / world.populations[team])

        # Plot initialization
        if not self.plotInitialized:

            self.plotInitialized = True

            for team in world.teams:
                # Population
                color = [i / 255 for i in colors[team]]
                color.append(1) # alpha
                self.plots['population'][team], = self.axes['population'].plot(self.x, self.data[team]['population'], color=color)

                # Genes and Actions
                for action in self.genes:
                    self.plots['genes'][action][team], = self.axes['genes'][action].plot(self.x, self.data[team]['genes'][action], color=color)
                    self.plots['actions'][action][team], = self.axes['actions'][action].plot(self.x, self.data[team]['actions'][action], color=color)

            # Set interactive mode
            plt.ion()
            plt.show()

        # Plot
        else:
            # Population
            self.axes['population'].set_xlim([0, world.epoch])

            for team in world.teams:
                if self.axes['population'].get_ylim()[1] < self.data[team]['population'][-1]:
                    self.axes['population'].set_ylim([0, 1.2 * self.axes['population'].get_ylim()[1]])

                self.plots['population'][team].set_xdata(self.x)
                self.plots['population'][team].set_ydata(self.data[team]['population'])

            # Genes and actions
            for action in self.genes:

                self.axes['genes'][action].set_xlim([0, world.epoch])
                self.axes['actions'][action].set_xlim([0, world.epoch])

                for team in world.teams:

                    if self.axes['actions'][action].get_ylim()[1] < self.data[team]['actions'][action][-1]:
                        self.axes['actions'][action].set_ylim([0, 1.2 * self.axes['actions'][action].get_ylim()[1]])

                    self.plots['actions'][action][team].set_xdata(self.x)
                    self.plots['actions'][action][team].set_ydata(self.data[team]['actions'][action])

                    if self.axes['genes'][action].get_ylim()[1] < self.data[team]['genes'][action][-1]:
                        self.axes['genes'][action].set_ylim([0, 1.2 * self.axes['genes'][action].get_ylim()[1]])

                    self.plots['genes'][action][team].set_xdata(self.x)
                    self.plots['genes'][action][team].set_ydata(self.data[team]['genes'][action])

            # Refresh plot
            self.figure.canvas.start_event_loop(0.001) # plt.pause(0.001) steals the focus