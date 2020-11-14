from matplotlib import pyplot as plt
from Constants import *
from matplotlib.gridspec import GridSpec


class Plot:

    def __init__(self, world):

        # Init data
        self.data = {'healthy': [], 'infected': [], 'deaths': [], 'cumDeaths': [], 'inmune': [], 'capacity': [systemCapacity, systemCapacity]}
        self.x = []
        self.plots = {'healthy': None, 'infected': None, 'deaths': None, 'cumDeaths': None, 'inmune': None, 'capacity': None}
        self.init = None
        self.figure, self.axes = plt.subplots()

        plt.title('Evolución virus')
        plt.xlabel('Tiempo')
        plt.ylabel('% Población inicial')
        self.axes.tick_params(labelright=True)

        self.previousDeaths = 0



    def update(self, world):

        popFactor = 100 / startingPopulation

        self.x.append(world.epoch)
        self.data['healthy'].append(world.data['healthy'] * popFactor)
        self.data['infected'].append(world.data['infected'] * popFactor)
        self.data['deaths'].append(world.data['deaths'] * popFactor)

        self.previousDeaths += self.data['deaths'][-1]
        self.data['cumDeaths'].append(self.previousDeaths)

        self.data['inmune'].append(world.data['inmune'] * popFactor)

        if not self.init:

            self.init = True

            self.plots['healthy'], = self.axes.plot(self.x, self.data['healthy'], 'b', label='Sanas')
            self.plots['infected'], = self.axes.plot(self.x, self.data['infected'], 'y', label='Infectadas')
            self.plots['deaths'], = self.axes.plot(self.x, self.data['deaths'], 'r', label='Muertes')
            self.plots['cumDeaths'], = self.axes.plot(self.x, self.data['cumDeaths'], 'k', label='Muertes acumuladas')
            self.plots['inmune'], = self.axes.plot(self.x, self.data['inmune'], 'g', label='Inmunes')
            self.plots['capacity'], = self.axes.plot([0, self.x[-1]], self.data['capacity'], 'm--', label='Capacidad del sistema')
            # self.axes.legend()
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.ion()
            plt.show()

        else:

            self.axes.set_xlim([0, world.epoch])
            self.axes.set_ylim([0, 105])

            self.plots['healthy'].set_xdata(self.x)
            self.plots['infected'].set_xdata(self.x)
            self.plots['deaths'].set_xdata(self.x)
            self.plots['cumDeaths'].set_xdata(self.x)
            self.plots['inmune'].set_xdata(self.x)
            self.plots['capacity'].set_xdata([0, self.x[-1]])

            self.plots['healthy'].set_ydata(self.data['healthy'])
            self.plots['infected'].set_ydata(self.data['infected'])
            self.plots['deaths'].set_ydata(self.data['deaths'])
            self.plots['cumDeaths'].set_ydata(self.data['cumDeaths'])
            self.plots['inmune'].set_ydata(self.data['inmune'])


        # Refresh plot
        self.figure.canvas.start_event_loop(0.001) # plt.pause(0.001) steals the focus