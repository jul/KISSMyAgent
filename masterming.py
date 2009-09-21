#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils.matrix import matrix
from utils.agent import *
from utils.graph import Representation
import numpy as np
import pdb

class Universe:
    "gère le temps et l'espace pour une simulation"
    matrix=None
    repres=None
    graph=None
    temp=1000
    
        
    def __init__(self,size_x,size_y,**args):
        from random import randint as rand
        
        for k in args.keys():
            setattr(self,k,args[k])
        self.matrix=matrix(size_x,size_y)
        ### init agent
        for i in range(0,size_x):
            for j in range(0,size_y):   
                  args=dict(x=i,y=j,utility=100)
                  self.matrix.set(
                                i,j, 
                                BoyScout(**args)   if rand(0,1) else ToutPourMaGueule(**args)
                                )
        ## init voisinage
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
    
    def next(self):
        self.matrix.get_rand().interaction()
        self.temp-=1 
        return self.temp >= 0

        
x=7
y=7
draw_time=400
u=Universe(x,y,temp=4000)
Desktop=Representation(universe=[ u ],nb_canvas=1,nb_graph=2)
Moyenne=Desktop.graph[0]
Total=Desktop.graph[1]


i=0
res=dict()
for k in MetaAgent.personalities:
    res[k]=[]
while u.next():
    i+=1
    res_temp=dict()
    perso_count=dict()
    for k in MetaAgent.personalities:
        res_temp[k]=0
        perso_count[k]=0
    for agent in u.matrix.as_table():
        res_temp[agent.personality]= res_temp[agent.personality] + agent.utility
        perso_count[agent.personality] += 1


    p=[]
    keys=[]
    m=[]
    m_keys=[]
    for perso in res_temp.keys():
        res[perso].append(res_temp[perso])


    if ( i % draw_time  == 0):
        Desktop.clear()
        for perso in res_temp.keys():
            p += [ Total.plot(res[perso])] 
            keys += [ "Total : %s (%d)" % (perso, res_temp[perso]) ]
        Total.legend(p,keys)
        for perso in res_temp.keys():
            m += [ Moyenne.plot( [ r/perso_count[perso] for r in res[perso] ]  )  ] 
            m_keys += [ "Moyenne : %s (%f)" % (perso, 1.0 * res_temp[perso] / perso_count[perso]  ) ]
        Moyenne.legend(m,m_keys)
        Desktop.plot_universe()
        Desktop.draw()    


Desktop.show()
