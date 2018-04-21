# Ant-colony-optimization
Python algorithm to find an optimized path through a graph

## Computation

*environment.py* embeds the class **environment**. This class is the one that should be used to compute the colony optimization. The method **step()** should be called every time you want to increment one step to your colony life. It performs various updates:

- Evaporates pheromones on the roads
- Ants secrete pheromones
- Ants walk one step
- If ants arrives in a new node, they choose a new road to follow. This decision can be random (to try new solutions) or based on the pheromone level of non visited roads. When ants reach food, they come back to their colony following the roads they took.

To initiate a new environment, the following parameters should be passed :

- **graph** : A 2D array containing distances between nodes. Every node corresponds to index of the array. Node 0 is always the colony and the last node is where the food is located.

- **nb_ants_max** : ??

- **nb_individuals** : ??????

- ** Revoir tous les paramètres en fait, tu les a modifiés**

- **evaporation_rate** : Rate of evaporation of pheromone on the roads. Pheromone is updated by multiplicating pheromone level on the road by (1 – evaporation_rate)

- **alpha** : Amount of pheromones left on road by every ants

- **randomness_rate** : Define the probability of random choice when ants arrive on a node

- **decision_threshold** : Define the probability of applying wether one decision formula or the other one .

To get best path, the method **best_path()** should be called. Best path is determined by choosing the road with maximum pheromone level at each node. It returns a list of nodes composing the path.

### Genetic mecanismes

We generate several environment with random parameters. Then we perform crossover and natural selection to select the environment settings that find the sortest path for a given graph.

### Graphical Modelling

The following description has to be red with the graphique.py file.

The first window we create manage the clicks of the user to create circles and balls to create the graph. 
So with the left click, we active the **draw-circle function** which conservs the position of the node in the Nods matrix. 
With the right click, we active the **onclick_handler** which is creating a new line and when we release the mouse, we end this line. To avoid some problems of position, we take the nearest node at the beginning and at the end of the line, so we're sure that a path is connecting two nods. It's the objective of the **Dist** matrix 

