#!/usr/bin/python
from utils.matrix import matrix
from utils.agent import Agent
from utils.graph import Representation

class Universe:
    matrix=None
    repres=None
    def __init__(self,size_x,size_y,**args):
        self.repres=Representation()
        for k in args.keys():
            setattr(self,k,args[k])
        self.matrix=matrix(size_x,size_y)

        for i in range(0,size_x):
            for j in range(0,size_y):   
                  self.matrix.set(
                                i,j,
                                Agent(x=i ,y=j ,
                                state= (i+j) % 3 > 0 ,repres=self.repres)
                                )
                  self.matrix.get(i,j).plot()
        for i in range(0,size_x):
            for j in range(0,size_y):   
                neigb=[]
                for coord in ( (0,1), (1,0), (-1,0), (0,-1) ):
                        dx,dy=coord
                        neigb.append(self.matrix.get(
                            (i+dx)%size_x,
                            (j+dy)%size_y
                            )
                        )

                self.matrix.get(i,j).neighbors(neigb)

        

    def show(self):
        self.repres.show()

u=Universe(3,3)

u.show()
