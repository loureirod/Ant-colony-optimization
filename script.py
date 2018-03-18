import numpy as np
import environment as env

graph = np.random.randint(1,10,(10,10))
number_ants = 100
evaporation_rate = 0.5
steps = 1000


environment = env.Environment(graph,number_ants,evaporation_rate)

for k in range(steps):
    environment.step()


print(environment.pheromone)