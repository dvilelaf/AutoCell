# Number of teams (max 5)
nTeams = 1

# World size (in cells)
worldWidth, worldHeight = 320, 180

# Cell parameters
startingPopulation = 10000          # World is initialized with 100 cells

nPatientZero = 2
infectionProbability = 0.5
deathProbability = 0.005
epochsToCure = 15
moveProb = 0.75
systemCapacity = 20

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
videoFPS = 10                           # Frames per second
videoPath = './simulation.mkv'          # Video path
lossless = False                        # Use lossless encoding?

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
