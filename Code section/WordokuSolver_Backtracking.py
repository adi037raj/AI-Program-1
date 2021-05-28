
from PyDictionary import PyDictionary 
import enchant 
import copy
import time



class Wordku(object):
    def __init__(self, grid):# intializing variables
       
        self.grid = grid # its a self.grid is a list of lists
        self.ans = copy.deepcopy(grid) # using deepcopy refrence
        self.n_o_a = 0      #the number for assignment
        self.n_o_e = 0     #th number of empty
        self.times=0
        #here we initialize everything and process will calculate the result t solve
      
    def isAssigned(self, i):
        return type(i) == int   #return true or false if its type int

    

    
  

    # it Returns False if result == fails, else return the constraint_satis_prob
    def back_trac(self, constraint_satis_prob):# for backtraing
        self.times+=1
        if self.checkit(constraint_satis_prob): #it returns if after check it found true
            return constraint_satis_prob

        # Get index of variable to assign
        var = self.pick_up_var(constraint_satis_prob)  # now selecting un_assigned variables
        set_of_doms = constraint_satis_prob[var[0]][var[1]] # find the set of domains
        for val in set_of_doms:
            constraint_satis_probcopy = copy.deepcopy(constraint_satis_prob) # Should be the only place required for deepcopy
            self.n_o_a += 1  #as no of assignment is increased
            constraint_satis_probcopy[var[0]][var[1]] = val # Assignment
            if self.constraint_satis_prob(constraint_satis_probcopy): # If inference never fail
                result = self.back_trac(constraint_satis_probcopy)
                if result != False: # If never fail
                    return result

        return False


    def checkit(self, constraint_satis_prob): #check whther the assignment complete
        for row in constraint_satis_prob: #traversing every csp
            for elem in row:
                if not self.isAssigned(elem): #if not assigned need further inverstigation
                    return False

        return True #everything seems fine

    def pick_up_var(self, constraint_satis_prob): #selecting Unassigned Variables
        vars = self.check_most_vars(constraint_satis_prob) #checking the most csp
        var = self.check_most_var(constraint_satis_prob, vars) 
        return var  #returning the unassigned variables

    def check_most_vars(self, constraint_satis_prob): #select the Most Constrained variables
        vars = (9, []) # (set_of_doms size, all vars with that set_of_doms size)
        for i in range(9):
            for j in range(9):
                set_of_doms = constraint_satis_prob[i][j]
                if type(set_of_doms) == int:  #checking type of domains to int
                    continue

                size = len(set_of_doms)
                if size == vars[0]:
                    vars[1].append((i,j))

                if size < vars[0]:
                    vars = (size, [(i,j)])

        return vars[1]

    def check_most_var(self, constraint_satis_prob, vars): #find the most_variavbles assigned
        most = (-1, None)
        for var in vars:
            numOfNeighbours = self.find_unassigned(constraint_satis_prob, var)
            if numOfNeighbours > most[0]:
                most = (numOfNeighbours, var)
        return most[1]

    def find_unassigned(self, constraint_satis_prob, var):#getting Number Of Unassigned Neighbours
        neighbours = self.find_neighbour(var)
        total = 0
        for neighbour in neighbours:
            if not self.isAssigned(constraint_satis_prob[neighbour[0]][neighbour[1]]):
                total += 1
        return total

    
    #index tuple row,col
    def find_neighbour(self, index): # get neighbouring constraints so to do backtrack if need

        neighbours = set()

        # col is same
        for row_index in range(0, 9):
            neighbours.add((row_index,index[1]))

        # row is same
        for col_index in range(0, 9):
            neighbours.add((index[0], col_index))

        t_l_b = (index[0] - (index[0] % 3), index[1] - (index[1] % 3))

        for i in range(t_l_b[0], t_l_b[0] + 3):
            for j in range(t_l_b[1], t_l_b[1] + 3):
                neighbours.add((i,j)) #appending it to the neighbhours
        
        neighbours.remove((index)) # Remove self
        return list(neighbours) #returning the list of neighbours


    
    # Returns False if not consistent
    def constraint_satis_prob(self, constraint_satis_prob): #using ac3 csp
        # define initial constraints into a queue
        q_c_t = []
        for row_index, row in enumerate(constraint_satis_prob):
            for col_index, value in enumerate(row):
                if not self.isAssigned(value):  # if variable
                    neighbours = self.find_neighbour((row_index, col_index))
                    constraints = [((row_index, col_index), neighbour) for neighbour in neighbours]
                    q_c_t += constraints

        while q_c_t:
            constraint = q_c_t.pop()
            if self.check_again(constraint_satis_prob, constraint[0], constraint[1]): #checking for constraint satisfaction
                if len(constraint_satis_prob[constraint[0][0]][constraint[0][1]]) == 0: #checking the lenght is zero or not
                    return False
                neighbouring_arcs = self.find_neighbour(constraint[0])
                neighbouring_arcs.remove(constraint[1])
                for arc in neighbouring_arcs: #again for neighbours check
                    if not self.isAssigned(constraint_satis_prob[arc[0]][arc[1]]):
                        q_c_t.append((arc, constraint[0]))

        return True

   
    def check_again(self, constraint_satis_prob, i, j): #type of revise
        iset_of_doms = constraint_satis_prob[i[0]][i[1]] # Must be a list, cannot be assigned
        jset_of_doms = constraint_satis_prob[j[0]][j[1]] # Might be already assigned, or a list
        if type(jset_of_doms) == int:
            if jset_of_doms in iset_of_doms:
                iset_of_doms.remove(jset_of_doms)
                return True
            else:
                return False
        
        if len(jset_of_doms) <= 1:
            if jset_of_doms[0] in iset_of_doms: #if its in the domain return true
                iset_of_doms.remove(jset_of_doms[0])
                return True
        
        return False
    def process(self):  
       
        
        initial_set_of_doms = [1,2,3,4,5,6,7,8,9]# the set_of_doms is from 1 to 9 which is mapped to certain character
        new_set_puzzle= copy.deepcopy(self.grid)
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    self.n_o_e += 1

        for row_index, row in enumerate(self.grid):
            for col_index, value in enumerate(row):
                if value == 0:
                    new_set_puzzle[row_index][col_index] = initial_set_of_doms[::]
                else:
                    new_set_puzzle[row_index][col_index] = value

        
        # Now looping in throught the queue tuple
        self.constraint_satis_prob(new_set_puzzle)
        result = self.back_trac(new_set_puzzle)
        return result

if __name__ == "__main__":
    t0= time.time()
   #opening the file to read
    input_file="input_6.txt"
    output_file="output_6.txt"
    f = open(input_file, 'r')
    
    

    grid = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    dict_for_chartoint={}
    dict_for_inttochar={}
    a=1
    b=1

    i, j = 0, 0
    for line in lines:
        for number in line:
            if 'A' <= number <= 'Z':
                
                
                if(dict_for_chartoint.get(number)==None):
                    dict_for_chartoint[number]=a
                    dict_for_inttochar[a]=number
                    a+=1
                   
               # print(number,dict_for_chartoint.get(number))
                grid[i][j] = dict_for_chartoint.get(number)
                j += 1
                if j == 9:
                 i += 1
                 j = 0
            if number=='*':
                grid[i][j]=0
                j += 1
                if j == 9:
                 i += 1
                 j = 0
                

    
#    print(grid)
    t3=time.time()
    wudoku = Wordku(grid)
    ans = wudoku.process()
    print("Nodes generated "+str(wudoku.times))
    
    t2=time.time()-t3
    check_str=""
    dict = enchant.Dict("en_US") 
    var=False
    for i in range(9):
         for j in range(9):
            print(str(dict_for_inttochar[ans[i][j]]), end =" ")
         print("")


    #writitng this answer to out.txt file
    with open(output_file, 'w') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(dict_for_inttochar[ans[i][j]]) + " ")
            f.write("\n")

# now we check for vaild word in row , col, body diagonal

    for i in range(9):
         for j in range(9):
            check_str+=dict_for_inttochar[ans[i][j]] #checking the row
         if dict.check(check_str)==True:
             print(check_str)
             var=True
             
         check_str=""
    
    for i in range(9):
         for j in range(9):
            check_str+=dict_for_inttochar[ans[j][i]] #checking the col
         if dict.check(check_str)==True:
             print(check_str)
             var=True
             
         check_str=""
    
    for i in range(9):
         for j in range(9):
             if i==j:
               check_str+=dict_for_inttochar[ans[j][i]] #checking the body diagonal
    
    if dict.check(check_str)==True:
             print(check_str)
             var=True
             
    if var==False:
        print("None word found ")
             
    t1 = time.time() - t0
    print("THE TOTAL TIME IS "+str(t1))
    print("The search Time is  "+str(t2))

   
