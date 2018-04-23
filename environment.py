import numpy as np

class Genetic:
    def __init__(self,nb_individuals,nb_ants_max,env_iterations,genetic_iterations,crossover_rate,mutations_rate,test_graph):
        self.population = [] # Contains [environment,best_path lenght]
        self.env_iterations = env_iterations
        self.genetic_iterations = genetic_iterations
        self.crossover_rate = crossover_rate
        self.mutations_rate = mutations_rate
        self.nb_individuals = nb_individuals
        self.test_graph = test_graph
        self.stored_best_individual = 0

        for k in range(nb_individuals):
            number_ants = np.random.randint(0,nb_ants_max)
            evaporation_rate = np.random.uniform(0,1)
            alpha = np.random.uniform(0,10)
            randomness_rate = np.random.uniform(0,1)
            decision_threshold = np.random.uniform(randomness_rate,1)

            self.population.append( [Environment(test_graph,number_ants,evaporation_rate,alpha,randomness_rate,decision_threshold),0] )

    def mutations(self):
        selected = np.random.choice([ind[0] for ind in self.population], int(self.nb_individuals * self.mutations_rate))

        for individual in selected:
            individual.number_ants = max(0, individual.number_ants + np.random.randint(-10,10))
            individual.evaporation_rate = max(0,individual.evaporation_rate + np.random.uniform(-0.1,0.1))
            individual.alpha = max(0, individual.alpha + np.random.uniform(-1,1))
            individual.randomness_rate = min(max(0,individual.randomness_rate + np.random.uniform(-0.5,0.5)),1)
            individual.decision_threshold = min(max(0,individual.decision_threshold + np.random.uniform(-0.5,0.5)),1)
            

    def crossover(self):
        for k in range(int(self.nb_individuals * self.crossover_rate)):
            self.population[k] = self.reproduction(self.population[k][0],self.population[k+1][0])


    def reproduction(self,individual1,individual2):

        number_ants = int(0.5 * (individual1.number_ants + individual2.number_ants))
        evaporation_rate = 0.5 * (individual1.evaporation_rate + individual2.evaporation_rate)
        alpha = 0.5 * (individual1.alpha + individual2.alpha)
        randomness_rate = 0.5 * (individual1.randomness_rate + individual2.randomness_rate)
        decision_threshold = 0.5 * (individual1.decision_threshold + individual2.decision_threshold)

        newborn = Environment(self.test_graph,number_ants,evaporation_rate,alpha,randomness_rate,decision_threshold)

        return [newborn,0]

    def evaluate(self,environment):

        environment.initialize_ant_population()
        for k in range(self.env_iterations):
            environment.step()

        return environment.best_path()[0]

    def selection(self):
        for k in range(self.nb_individuals):
            self.population[k][1] = self.evaluate(self.population[k][0])

        self.population = sorted(self.population, key=lambda x: x[1])

    def animate(self):
        for k in range(self.genetic_iterations):
            print("Generation: " + str(k+1) + "/" + str(self.genetic_iterations))
            self.crossover()
            self.mutations()
            self.selection()

    def best_individual(self):
        
        return self.population[0][0]

    def print_best_individual_params(self):
        print("## Best individual parameters ##")
        print("Alpha:" + str(self.stored_best_individual.alpha))
        print("Randomness rate:" + str(self.stored_best_individual.randomness_rate))
        print("Decision threshold:" + str(self.stored_best_individual.decision_threshold))
        print("Number of ants:" + str(self.stored_best_individual.number_ants))
        print("Evaporation rate:" + str(self.stored_best_individual.evaporation_rate))
        print("Best path:" + str(self.stored_best_individual.stored_best_path[1]))
        print("Best path lenght:" + str(self.stored_best_individual.stored_best_path[0]))
        
        

    def compute_best_individual(self):
        self.animate()
        self.stored_best_individual = self.population[0][0]
        self.stored_best_individual.initialize_ant_population()
        return self.stored_best_individual


class Environment:
    def __init__(self,graph,number_ants,evaporation_rate,alpha,randomness_rate,decision_threshold):
        self.graph = np.copy(graph)  # Matrix of distances between node i and j
        self.number_ants = number_ants
        self.evaporation_rate = evaporation_rate
        self.step_counter = 0
        self.alpha = alpha
        self.randomness_rate = np.random.uniform(0,randomness_rate)
        self.decision_threshold = decision_threshold
        self.stored_best_path = [0,[0]] # best_path lenght, best_path nodes

        self.initialize_ant_population()

        

    def initialize_ant_population(self):
        self.population = []
        self.pheromone = np.zeros_like(self.graph) # Matrix of pheromone level between node i and j

        for k in range(self.number_ants):
            self.population.append( Ant(self.alpha,self.randomness_rate,self.decision_threshold) )

    def evaporate(self):
        self.pheromone = (1-self.evaporation_rate) * self.pheromone


    def step(self):

        self.evaporate()

        for ant in self.population:

            if ant.road_step == self.graph[ant.road[0],ant.road[1]]: #Ant reached node
                
                if ant.road[1] == np.shape(self.graph)[1]-1:  #Node is the food node
                    ant.state = "backward"

                if ant.road[1] == 0:  #Node is the colony node
                    ant.state = "forward"
                    ant.visited_nodes = []  #Memory is erased


                ant.decide(self.pheromone,self.graph)
                if ant.state != "backward":
                    ant.secrete(self.pheromone)

            else:

                ant.walk()
        

    def best_path(self):
        '''Return current best path. Best path is determined by choosing the road with maximum pheromone level at each node '''

        food_node = np.shape(self.pheromone)[0] - 1
        visited_nodes = []
        city = 0
        lenght = 0

        while city != food_node:

            visited_nodes.append(city)
            
            city_pheromones = self.pheromone[city,:]

            city_pheromones[visited_nodes] = 0

            if np.nonzero(city_pheromones)[0].size == 0:
                return np.inf, "Food node is not on the current best path"

            new_city = np.argmax(city_pheromones) #Select best node that hasn't been visited

            lenght = lenght + self.graph[city,new_city]

            city = new_city

        visited_nodes.append(city)

        self.stored_best_path = [lenght,visited_nodes]

        return lenght,visited_nodes    



class Ant:
    def __init__(self,alpha,randomness_rate,decision_threshold):
        self.alpha = alpha
        self.beta = np.random.uniform(-5,5)
        self.gamma = np.random.uniform(-5,5)
        self.delta = np.random.uniform(1,2)    #For decision
        self.sigma = np.random.uniform(0,0)    #For decision (Heuristique)      
        self.state = "forward" #forward,backward
        self.visited_nodes = [0]
        self.newcomer =  True # Enables random decision at begining
        self.selection = "lambda"
        self.road = [0,0]
        self.road_step = 0
        self.randomness_rate = randomness_rate
        self.decision_threshold = decision_threshold

        

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

            possibilities = np.copy(graph[city,:])
            possibilities[self.visited_nodes] = 0

            if np.nonzero(possibilities)[0].size == 0 or self.newcomer: # There is no more unvisited node (She is chasing her tail) or she is a newcomer
                new_city = np.random.choice(np.nonzero(graph[city,:])[0])

                if self.newcomer:
                    self.newcomer = False

            else: # Normal case

                if np.random.uniform(0,1) > self.randomness_rate: # Deterministic decision
                    if np.random.uniform(0,1) < self.decision_threshold: # First type decision

                        estimator = np.power(self.heuristic(graph[city,:]),self.sigma) * pheromone[city,:]

                        estimator[self.visited_nodes] = 0

                        if np.max(estimator)==0: # Optimal choice can't be made
                            new_city = np.random.choice(np.nonzero(possibilities)[0])
                        else:
                            new_city = np.argmax(estimator) #Select best node that hasn't been visited

                    else: # Second type decision

                        intermediate = np.power(self.heuristic(graph[city,:]),self.sigma) * np.power(pheromone[city,:],self.delta)
                        S = np.sum(intermediate)

                        if S==0: #No road from city has ever been visited
                            possibilities = np.copy(graph[city,:])

                            new_city = np.random.choice(np.nonzero(possibilities)[0])

                        else:

                            estimator = 1/S * np.power(self.heuristic(graph[city,:]),self.sigma) * np.power(pheromone[city,:],self.delta)

                            estimator[self.visited_nodes] = 0

                            if np.max(estimator)==0: # Optimal choice can't be made
                                new_city = np.random.choice(np.nonzero(possibilities)[0])
                            else:
                                new_city = np.argmax(estimator) #Select best node that hasn't been visited

                else: # Random decision

                    possibilities = np.copy(graph[city,:])
                    possibilities[self.visited_nodes] = 0

                    new_city = np.random.choice(np.nonzero(possibilities)[0])


            self.road = [city,new_city]
            self.road_step = 0
            self.visited_nodes.append(city)



    def secrete(self,pheromone):
        '''Secrete pheromones on the road. To be called after decide'''
        i,j = self.road

        # pheromone[i,j] = self.alpha * np.abs(np.sin( self.beta * pheromone[i,j] + self.gamma ))

        pheromone[i,j] =  pheromone[i,j] + self.alpha
        
        pheromone[j,i] = pheromone[i,j]
    
    def walk(self):
        ''''Increment road step'''
        self.road_step += 1



if __name__ == '__main__':

    graph = np.array([[0,3,1,4,0],[3,0,1,0,1],[1,1,0,1,3],[4,0,1,0,4],[0,1,3,4,0]],dtype='float32')
    nb_individuals = 10
    nb_ants_max = 100
    env_iterations = 100
    genetic_iterations = 5
    crossover_rate = 0.30
    mutations_rate = 0.30

    genetic = Genetic(nb_individuals,nb_ants_max,env_iterations,genetic_iterations,crossover_rate,mutations_rate,graph)
    environment = genetic.compute_best_individual()
    genetic.print_best_individual_params()

    print("--Code executed--")
