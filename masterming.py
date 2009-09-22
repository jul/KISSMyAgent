#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils.matrix import matrix
from utils.agent import *
from utils.graph import Representation
from utils.universe import Universe
import numpy as np
import pdb

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
