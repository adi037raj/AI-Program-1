import random
import copy
import math
import numpy as np

def myfunction_to_fitness(x):
    dc = 0
    hc = sum([x.count(i)-1 for i in x])/2
    length = len(x)
    ld = [0] * 2*length
    rd = [0] * 2*length
    for i in range(length):
        ld[i + x[i] - 1] += 1
        rd[len(x) - i + x[i] - 2] += 1

    dc = 0
    for i in range(2*length-1):
        c = 0
        if ld[i] > 1:
            c += ld[i]
        if rd[i] > 1:
            c += rd[i]
        dc += c
    
    
    #print(hc+dc)
    kk=-hc-dc
    #fitness value is negative of conflicts 
    print("individuals = {}  fitness = {}".format(x,kk))
    return int(-(hc + dc))



def fitness(individual):
    
      return myfunction_to_fitness(individual)

mutation_prob=4 #providing the probabilty in percentage
crossover_prob=10
def crossover(individual1, individual2):
    
     rr=random.randomint(1,100)
     if rr<=crossover_prob:
         return individual1 #checking the prob if otherwise just return anyone individual
    #in cross over we generate 2 child and if prob is less than 3% then we mutate otherwise leave as it is
     n=len(individual1)
     a = random.randint(0,  n- 1) 
     b = random.randint(0, n - 1)
     
     c=individual1[0:a] + individual2[a:(n)]
     d=individual1[0:b] + individual2[b:(n)]
     rr=random.randomint(1,100)
     if rr<=mutation_prob:
         mutation(c)
         
     if rr<=mutation_prob:
         mutation(d)
        
         
     return c[0:a] + d[a:len(individual1)]
    

def mutation(individual):
    
   
    a = random.randint(0, len(individual) - 1)
    b = random.randint(1, len(individual))
    individual[a] = b
    return individual
    

def first_two_value(f):
    f.sort()
    if len(f)==1:
        return f[0],f[0]
    return f[0],f[1]
    
    

def generate_individual(n):
    result = list(range(1, n + 1))
    np.random.shuffle(result)
    return result

class Genetic(object):

    def __init__(self, n ,pop_size):
        #initializing a random individuals with size of initial population entered by user
        self.queens = []
        for i in range(pop_size):
            self.queens.append(generate_individual(n))
    
  
    

    #generating individuals for a single iteration of algorithm
    def generate_population(self, random_selections=5):
        
        
        candid_parents = []
        candid_fitness = []
        k={}
        #getting individuals from queens randomly for an iteration
        for i in range(random_selections):
            candid_parents.append(self.queens[random.randint(0, len(self.queens) - 1)])
            candid_fitness.append(fitness(candid_parents[i]))
            k.update({candid_fitness[i]:candid_parents[i]})
        sorted_fitness = copy.deepcopy(candid_fitness)
        #sort the fitnesses of individuals 
        sorted_fitness.sort()
        #print(sorted_fitness)
        
        

        
                
        individuals = crossover(sorted_fitness[0],sorted_fitness[1]) #sending the first 2 value as it is sorted now,we can also use a minheap like structure but it becomes tidius 
        
      
        mutation(individuals)
        
       
        indi_fitness = fitness(individuals)#in the following code we check that child is better than every queens,then set the new child
        for i in self.queens:
            if(indi_fitness<fitness(i)):
                self.queens.append(individuals)
                self.queens.remove(i)
                break

    def finished(self):
         
          for j in self.queens:
            if(fitness(j)==0):
             return [True,j]#return it as a list
          return [False]
            
            
           
            #here we check that for every queen there no attacking now becomes easier to use attacking in fitness pairs instead of not attacking

    def start(self, random_selections=5):
        #generate new population and start algorithm until number of attacking pairs is zero
        while not self.finished()[0]:
            self.generate_population(random_selections)
        final_state = self.finished()
        print(('Solution : ' + str(final_state[1])))
        print("fitness value "+str(fitness(final_state[1])))
        
       

#******************** N-Queen Problem With GA Algorithm ***********************

n=(int)(input('Enter the value of N \n -'))
initial_population=(int)(input('Enter initial population size \n -'))
maxFitness=(n*(n-1))/2
algorithm = Genetic(n=n,pop_size=initial_population)
algorithm.start()
