#!/usr/bin/python
from utils.matrix import matrix
from utils.agent import *
from utils.graph import Representation
import pdb

class Universe:
    matrix=None
    repres=None
    graph=None

    def plot(self,i,j):
        self.repres.dot(i,j,self.matrix.get(i,j).color())

    def plot_agent(self,agent=None):
        x,y = agent.coord()
        self.repres.dot(x,y,agent.color())
        
    def __init__(self,size_x,size_y,**args):
        from random import randint as rand
        self.repres=Representation()
        for k in args.keys():
            setattr(self,k,args[k])
        self.matrix=matrix(size_x,size_y)
        for i in range(0,size_x):
            for j in range(0,size_y):   
                  args=dict(x=i,y=j,utility=100)
                  self.matrix.set(
                                i,j, 
                                BoyScout(**args)   if rand(0,1) else ToutPourMaGueule(**args)
                                )
                  self.plot(i,j)
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
        for a in self.matrix.as_table():
            print a
            self.plot_agent(a)
        self.repres.draw()
    def show(self):
        self.repres.show()
x=20
y=20
max_temp=2000
draw_time=100
u=Universe(x,y)
res=dict()
for k in MetaAgent.personalities:
    res[k]=[]

for i in range(0, max_temp):
    u.matrix.get_rand().interaction()
    if ( i % draw_time  == 0):
        u.draw()    
    res_temp=dict()
    for k in MetaAgent.personalities:
        res_temp[k]=0
    for agent in u.matrix.as_table():
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
