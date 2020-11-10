# AutoCell

Autocell is a cellular automaton written in Python. It uses pygame to show the system
evolution, plots population evolution and writes the simulation's video using openCV.

![Simulation](https://i.giphy.com/media/28I0Buot31cKedBvfT/giphy.webp)

![Imgur](https://i.imgur.com/9vycWbS.png)

## System rules

You can change the system parameters at *Constants.py*.

* The system is a *spherical* world, like in Pacman game: there are no limits. If a cell moves up the upper window end, it appears on the lower end. Also from left to right.
* There are 1 to 5 color-based teams.
* The system is randomly initialized with an initial population of cells.
* A cell has life points and age. It is alive while its life points are positive, its age is lower that the maximum age and there are fewer neighbours than the maximum. Its color will depend on its life points and age. Brighter means younger and healthier.
* At every epoch, every living cell, in a random order, must take an action that affects the system.
* Its possible actions depend on their 8 neighbour cells.
* A cell can wait, move, mate, attack or change teams.
* A cell has 5 different genes that marks its inclinations towards those actions. Also, every gen has an initial weight that can be changed.


### Waiting

* Waiting is always possible. No action is taken.


### Moving

* Movement is only posible if there is a neighbouring empty space.
* The more empty neighbours are around, the higher the change to move.


### Mating

* Mating is only posible if there is a neighbouring empty space for the child cell and another same-team cell to serve as the other parent.
* Mating only requires one cell to decide mating. It just copies its other-parent neighbour genes.
* Mating makes the decision-making parent to lose a certain % of its life points.
* A newborn cell inherits its parents gene averages, but has a chance of mutation.
* The more same-team neighbours are around, the higher the change to mate.


### Attacking

* Attackingis only posible if there is a different-team neighbour.
* The more different-team neighbours are around, the higher the change to attack.
* Attacking a cell means that both cells see their life points decreased until one of them dies.


### Changing teams

* Changing teams is only posible if there is a different-team neighbour.
* The more different-team neighbours are around, the higher the change to change team.



## Plots and videos

Plotting and video writting can be deactivated, as they make the simulation slower.