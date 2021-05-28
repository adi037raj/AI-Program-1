import time
import random
import copy
def isValidWordku(puzzle):   #to check whether the generated worduku is valid or not
        
        # Check rows
        for i in range(9):
            d = {}  # taking it as a set and finding whetehr all contraints are satisfied or not
            for j in range(9):
                if puzzle[i][j] == '.': #if its space or something
                    pass
                elif puzzle[i][j] in d: 
                    return False
                else:
                    d[puzzle[i][j]] = True
        # Check columns
        for j in range(9):  #doing the same with the every columns
            d = {}
            for i in range(9):
                if puzzle[i][j] == '.':
                    pass
                elif puzzle[i][j] in d:
                    return False
                else:
                    d[puzzle[i][j]] = True
        # Check sub-boxes
        for m in range(0, 9, 3):  # Now checking the grids and finding whether the wordku is valid or not
            for n in range(0, 9, 3):
                d = {}
                for i in range(n, n + 3):
                    for j in range(m, m + 3):
                        if puzzle[i][j] == '.':
                            pass
                        elif puzzle[i][j] in d:
                            return False
                        else:
                            d[puzzle[i][j]] = True
        return True


def checkme(puzzle,row,col,element):  # function to find whether element will go in place i,j of puzzle
# return true when the element got the right position , else return false
    
    # check in that row
    for j in range(9):
        if puzzle[row][j]==element:
            return False
    
    # in col
    for j in range(9):
        if puzzle[j][col]==element:
            return False
    
    
    #now chwck the grid:
    if(row<=2):
        if col<=2:
            for i in range(3):
                for j in range (3):
                    if puzzle[i][j]==element:
                                return False
        
        elif col>2 and col <6:
             for i in range(3):
                for j in range (3,6):
                    if puzzle[i][j]==element:
                                return False
        else:
            for i in range(3):
                for j in range (6,9):
                    if puzzle[i][j]==element:
                                return False
        
        
    elif row>2 and row<6:
         if col<=2:
            for i in range(3,6):
                for j in range (3):
                    if puzzle[i][j]==element:
                                return False
        
         elif col>2 and col <6:
             for i in range(3,6):
                for j in range (3,6):
                    if puzzle[i][j]==element:
                                return False
         else:
            for i in range(3,6):
                for j in range (6,9):
                    if puzzle[i][j]==element:
                                return False
        
        
        
    else:
         if col<=2:
            for i in range(6,9):
                for j in range (3):
                    if puzzle[i][j]==element:
                                return False
        
         elif col>2 and col <6:
             for i in range(6,9):
                for j in range (3,6):
                    if puzzle[i][j]==element:
                                return False
         else:
            for i in range(6,9):
                for j in range (6,9):
                    if puzzle[i][j]==element:
                                return False
         
    
    
    
    
    return True                    # it means everything goes fine and there is no conflict in row,col,grid

def myfunction(puzzle):
  
   
   for i in range(9):
        for j in range(9):
            if puzzle[i][j]==0:
                 for _ in range (1000000):
                    r=random.randint(1, 9)
                    if checkme(puzzle, i, j, r):
                        puzzle[i][j]=r
                        break
                
   
   return puzzle
   
    
               
                
    
    
   
            
    
    


if __name__ == "__main__":
   #opening the file to read
    t0=time.time()
    filename="input_3.txt"
    outfile="output_3.txt"
    f = open(filename, 'r')
  
    

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
                

    t3=time.time()
    check_str=""
    ans=myfunction(grid)
    
    t2=time.time()-t3
    
    if isValidWordku(ans):
    
     for i in range(9):
        for j in range(9):
            
                
            print(str(dict_for_inttochar[ans[i][j]]), end =" ")
        print("")
     with open(outfile, 'w') as f:
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
    else:
        print("The worduku isnt solved under the given steps")         
        
    t1 = time.time() - t0
    print("THE TOTAL TIME IS "+str(t1))
    print("The search Time is  "+str(t2))
   

    
    
    
    
    
    
    
    
    
    
    
    
    
    