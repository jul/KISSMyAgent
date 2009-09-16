#!/usr/bin/python
# -*- coding: utf-8 -*-

class matrix:
    matrix=[]
    size_x=None
    size_y=None
    def as_table(self):
        return self.matrix
    def __init__(self,size_x,size_y):
        self.size_y=size_y
        self.size_x=size_x
        self.matrix= [ None for i in range(0,size_x*size_y) ]

    def get_rand(self):
        from random import randint 

        return self.matrix[ randint(0,self.size_y * self.size_x -1 ) ]

    def get(self,x,y):
        return self.matrix[y*self.size_x+x]
    
    def set(self,x,y,val):
        self.matrix[y*self.size_x+x]=val

    def __str__(self):
        to_print="  "
        
        for x in range(0,self.size_x):
            to_print+="%d " % x 

        for cursor in range(0,self.size_x*self.size_y):
            cur_val=self.matrix[cursor]
            if (cursor %self.size_x==0):
                to_print+="\n%d " % (( cursor  ) / self.size_y)
            if (cursor%(self.size_x)!=0):
                to_print+=" "
            to_print+=str( cur_val ) if cur_val else "X"
        return to_print
def matrix_check():
#matrice 2x2
    m=matrix(3,2)
    # haut à gauche
    m.set(0,0,1)
    # haut mil
    m.set(1,0,2)
    m.set(2,0,3)
    #mil bas
    m.set(1,1,7)
    print(m)
    print(u""" 
résultat souhaité : 
  0 1 2
0 1 2 3
1 X 7 X
""")
if __name__ == '__main__':
    matrix_check()
