#!/usr/bin/python
from utils.matrix import matrix
from utils.agent import Agent
from utils.graph import Representation
import pdb

class Universe:
    matrix=None
    repres=None
    graph=None
    def __init__(self,size_x,size_y,**args):
        from random import randint as rand
        pers=[ "only_take" , "boy_scout" ] 
        self.repres=Representation()
        for k in args.keys():
            setattr(self,k,args[k])
        self.matrix=matrix(size_x,size_y)

        for i in range(0,size_x):
            for j in range(0,size_y):   
                  self.matrix.set(
                                i,j,
                                Agent(x=i ,y=j ,
                                        repres=self.repres,
                                        personality = pers[ 
                                            ## a mettre en param
                                            rand(0,1 )
                                        ],
                                        utility = 100,
                                    ),
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

                self.matrix.get(i,j).neighbors=neigb

        
    def draw(self):
        self.repres.draw()
    def show(self):
        self.repres.show()
x=10
y=10
max_temp=1000
u=Universe(x,y)
res=dict()
for k in Agent.personalities:
    res[k]=[]

for i in range(0, max_temp):
    u.matrix.get_rand().interaction()
    if ( i % 500 == 0):
        u.draw()    
    res_temp=dict()
    for k in Agent.personalities:
        res_temp[k]=0
    for agent in u.matrix.matrix[0:x*y]:
        res_temp[agent.personality]= res_temp[agent.personality] + agent.utility

    u.repres.graph.clear()
    p=[]
    keys=[]
    for perso in res_temp.keys():
        res[perso].append(res_temp[perso])
        p.append(u.repres.graph.plot(res[perso]))
        keys.append("%s (%d)" % (perso, res_temp[perso]))
    u.repres.graph.legend(p,keys)


u.show()
