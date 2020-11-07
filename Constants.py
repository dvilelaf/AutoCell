# Number of teams (max 5)
nTeams = 2

# World size (in cells)
worldWidth, worldHeight = 100, 100

# Cell parameters
startingPopulation = 100
cellMaxAge = 10
cellMaxLifePoints = 100
cellMinStartingLifeFactor = 0.75 # A cell is randomly initialized with between 75 and 100 life points
cellMatingFactor = 0.25 # A cell loses 25% of its life points when mating

# Window
windowWidth, windowHeight = 800, 800 # Window pixel size
gridOn = False # Show grid

# Colors
colors = {'blue':      (102, 194, 255),
          'red':       (255, 102, 102),
          'green':     (0, 204, 102),
          'yellow':    (255, 255, 179),
          'white':     (255, 255, 255),
          'darkGray':  (25, 25, 25),
          'lightGray': (100, 100, 100)}

backgroundColor = colors['darkGray']
gridColor = colors['lightGray']