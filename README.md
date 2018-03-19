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

- **number_ants** : Number of ants working in the environment


- **evaporation_rate** : Rate of evaporation of pheromone on the roads. Pheromone is updated by multiplicating pheromone level on the road by (1 – evaporation_rate)

To get best path, the method **best_path()** should be called. Best path is determined by choosing the road with maximum pheromone level at each node. It returns a list of nodes composing the path.
