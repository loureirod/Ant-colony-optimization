import numpy as np

class Environment:
    def __init__(self,graph,number_ants,evaporation_rate):
        self.graph = graph  # Matrix of distances between node i and j
        self.pheromone = np.zeros_like(graph) # Matrix of pheromone level between node i and j
        self.number_ants = number_ants
        self.population = []
        self.evaporation_rate = evaporation_rate

        #Create population
        for k in range(self.number_ants):
            self.population.append( Ant() )

    def evaporate(self):
        self.pheromone = (1-self.evaporation_rate) * self.pheromone


    def step(self):

        self.evaporate()

        for ant in self.population:

            if ant.road_step == graph[ant.road[0],ant.road[1]]: #Ant reached node
                
                if ant.road[1] == np.shape(graph)[1]-1:  #Node is the food node
                    ant.state = "backward"

                if ant.road[1] == 0:  #Node is the colony node
                    ant.state = "forward"
                    ant.visited_nodes = []  #Memory is ereased


                ant.decide(self.pheromone,self.graph)
                ant.secrete(self.pheromone)

            else:

                ant.walk()

    def best_path(self):
        '''Return current best path. Best path is determined by choosing the road with maximum pheromone level at each node '''

        food_node = np.shape(self.pheromone)[0] - 1
        visited_nodes = []
        city = 0

        while city != food_node:

            visited_nodes.append(city)
            
            city_pheromones = self.pheromone[city,:]

            city_pheromones[visited_nodes] = 0

            city = np.argmax(city_pheromones) #Select best node that hasn't been visited

        visited_nodes.append(city)

        return visited_nodes



class Ant:
    def __init__(self):
        self.alpha = np.random.uniform(0,5)
        self.beta = np.random.uniform(-5,5)
        self.gamma = np.random.uniform(-5,5)
        self.delta = np.random.uniform(0,1)    #For decision
        self.sigma = np.random.uniform(0,1)    #For decision        
        self.state = "forward" #forward,backward
        self.visited_nodes = []
        self.selection = "lambda"
        self.road = [0,0]
        self.road_step = 0
        self.randomness_rate = np.random.uniform(0,1)
        self.decision_threshold = np.random.uniform(0,self.randomness_rate)
        

    def heuristic(self,distances):
        '''Weights distances and annulate roads that doesn't exists'''

        result = np.zeros_like(distances)

        for k,distance in enumerate(distances):
            if distance != 0:
                result[k] = 1/distance

        return result


    def decide(self,pheromone,graph):
        '''Decide which road to take and memorize previous walk if nescessary'''

        city = self.road[1]

        if self.state == "backward":

            new_city = self.visited_nodes.pop()
            self.road = [city , new_city]
            self.road_step = 0

        else: # State is forward

            if np.random.uniform(0,1) < self.randomness_rate: # Random decision or not
                if np.random.uniform(0,1) < self.decision_threshold: 

                    estimator = np.power(self.heuristic(graph[city,:]),self.delta) * pheromone[city,:]

                    estimator[self.visited_nodes + [city]] = 0

                    new_city = np.argmax(estimator) #Select best node that hasn't been visited

                else:

                    intermediate = np.power(self.heuristic(graph[city,:]),self.sigma) * np.power(pheromone[city,:],self.delta)
                    S = np.sum(intermediate) - intermediate[city]

                    if S==0: #No road from city has ever been visited
                        possibilities = graph[city,:]
                        possibilities[city] = 0

                        new_city = np.random.choice(np.nonzero(possibilities)[0])

                    else:

                        estimator = 1/S * np.power(self.heuristic(graph[city,:]),self.sigma) * np.power(pheromone[city,:],self.delta)

                        estimator[self.visited_nodes + [city]] = 0

                        new_city = np.argmax(estimator) #Select best node that hasn't been visited

            else:

                possibilities = graph[city,:]
                possibilities[self.visited_nodes + [city]] = 0

                new_city = np.random.choice(np.nonzero(possibilities)[0])


            self.road = [city,new_city]
            self.road_step = 0
            self.visited_nodes.append(city)



    def secrete(self,pheromone):
        '''Secrete pheromones on the road. To be called after decide'''
        i,j = self.road
        pheromone[i,j] = self.alpha * np.abs(np.sin( self.beta * pheromone[i,j] + self.gamma ))
        pheromone[j,i] = pheromone[i,j]
    
    def walk(self):
        ''''Increment road step'''
        self.road_step += 1



if __name__ == '__main__':

    graph = np.array([[0,3,1,4,0],[3,0,1,0,1],[1,1,0,1,3],[4,0,1,0,4],[0,1,3,4,0]],dtype='float32')
    number_ants = 100
    evaporation_rate = 0.5
    steps = 1000

    environment = Environment(graph,number_ants,evaporation_rate)

    for k in range(steps):
        environment.step()

    print('Pheromone levels:')
    print(np.around(environment.pheromone,2))
    print('Best path:')
    print(environment.best_path())

    print("--Code executed--")
