# Number of teams (max 5)
nTeams = 3

# World size (in cells)
worldWidth, worldHeight = 320, 180

# Cell parameters
startingPopulation = 500          # World is initialized with 100 cells
cellMaxAge = 10                   # Cells die at ~10 epochs
cellMaxAgeVariance = 0.2          # Cell max age can be +-20%
cellMaxLifePoints = 100           # Cells have a maximum of ~100 life points
cellMaxLifePointsVariance = 0.2   # Cells max life points can be +-20%
cellMinStartingLifeFactor = 0.75  # A cell is randomly initialized with between 75 and 100 life points
cellMatingCost = 25             # A cell loses 25 of its life points when mating
cellMutationRate = 0.1            # A newborn cell mutates all its genes with a probability of 10%

# Genetic mask: relative weight of every gen (inclination towards an action)
geneticMask = {'blue':   {'wait': 1, 'move': 1, 'mate': 1, 'attack': 1, 'changeTeam': 1},
               'red':    {'wait': 1, 'move': 1, 'mate': 1, 'attack': 1, 'changeTeam': 1},
               'green':  {'wait': 1, 'move': 1, 'mate': 1, 'attack': 1, 'changeTeam': 1},
               'yellow': {'wait': 1, 'move': 1, 'mate': 1, 'attack': 1, 'changeTeam': 1},
               'white':  {'wait': 1, 'move': 1, 'mate': 1, 'attack': 1, 'changeTeam': 1}}

# Resources
neighbourLimit = 8  # 8 for no resource competition

# OUTPUT --------------------------------------------------------------------------------------

# Print data
logData = True                          # Print data for every step

# Window
showWindow = True                       # Show the simulation window
windowWidth, windowHeight = 1920, 1080  # Window pixel size
gridOn = False                          # Show grid
frameWait = 0.1                         # Time to wait between frames

# Plot
showPlot = True                         # Show plots (slower)

# Video
writeVideo = True                       # Save sim to video
videoWidth, videoHeight = 1920, 1080    # Video pixel size
videoFPS = 20                           # Frames per second
videoPath = './simulation.mkv'          # Video path

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
