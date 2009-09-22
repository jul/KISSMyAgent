#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils.matrix import matrix
from utils.agent import *
from utils.graph import Representation
from utils.universe import Universe
import numpy as np
import pdb

x=20
y=20
draw_time=500
args=dict( size_x= x, size_y= y, temp= 10000 )

args["agent_args"]=dict( can_bankrupt = False )
u=Universe(**args)

args["agent_args"]=dict( can_bankrupt = True )
u2=Universe(**args)

Desktop=Representation(universe=[ u,u2 ],nb_canvas=2,nb_graph=3,x=20,y=12)
Moyenne=Desktop.graph[1]
Transac=Desktop.graph[0]
#Total=Desktop.graph[2]
Moyenne_p=Desktop.graph[2]
u2.matrix.matrix = [ a.clone( can_bankrupt = True ) for a in  u.matrix.as_table() ] 
u2.set_neighb()

def small_leg(leg):
    for t in leg.get_texts():
        t.set_fontsize('small')

for a in u2.matrix.matrix:
    print a
i=0
res=dict()
res_pert=dict()
transac_by_perso=dict()
for k in MetaAgent.personalities:
    res[k]=[]
    res_pert[k]=[]
    transac_by_perso[k]=[ 0 ]
Desktop.plot_universe()
while u.next():
    print "interaction sans bkrupt"
    i+=1
    ( x , y ) =  u.current_agent.coord()
    agent=u2.matrix.get(x,y)
    if (u.current_agent.current_partner) :
        (px, py) =u.matrix.get(x,y).current_partner.coord()
        partner = u2.matrix.get(px,py)
        if partner and  agent.interaction(partner):
            agent.deal_with(partner)

    print "interaction a bkrupt"
    res_temp=dict()
    res_temp_pert=dict()
    perso_count=dict()

    for k in MetaAgent.personalities:
        res_temp[k]=0
        res_temp_pert[k]=0
        perso_count[k]=0

    for agent in u2.matrix.as_table():
        res_temp_pert[agent.personality] +=  agent.utility
    
    for agent in u.matrix.as_table():
        res_temp[agent.personality] +=  agent.utility
        perso_count[agent.personality] += 1
    t=[]
    t_keys=[]
    p=[]
    keys=[]
    m=[]
    m_keys=[]
    for perso in res_temp.keys():
        res[perso] += [ res_temp[perso] ]
        res_pert[perso] += [ res_temp_pert[perso] ]

    for perso in transac_by_perso.keys():
        array_val= transac_by_perso[perso]
        toadd  = 1 if ( u.current_agent.personality == perso ) else 0  
        toadd +=   array_val[-1] if len(array_val) else 0 
        array_val.append( toadd )

    if ( i % draw_time  == 0):

        Desktop.clear()
   #     for perso in res_temp.keys():
   #         p += [ Total.plot(res[perso])] 
   #         keys += [ "Total : %s (%d)" % (perso, res_temp[perso]) ]
   #     Total.legend(p,keys)
        for perso in MetaAgent.personalities:
            print "l %d,%d" % ( len(transac_by_perso[perso]) , i )
            t += [ Transac.plot(  transac_by_perso[perso] )  ]
            t_keys+= [ "Transac / perso : %s " % perso ]
        small_leg(Transac.legend(t,t_keys))
        print res_temp_pert
        print res_temp
        for perso in res_temp_pert.keys():
            m += [ Moyenne_p.plot( [ r/perso_count[perso] for r in res_pert[perso] ]  )  ] 
            m_keys += [ "w_b : %s (%.2f)" % (perso, 1.0 * res_temp_pert[perso] / perso_count[perso]  ) ]
        small_leg(Moyenne_p.legend(m,m_keys))
        m=[]
        m_keys=[]
        for perso in res_temp.keys():
            m += [ Moyenne.plot( [ r/perso_count[perso] for r in res[perso] ]  )  ] 
            m_keys += [ "w_o b : %s (%.2f)" % (perso, 1.0 * res_temp[perso] / perso_count[perso]  ) ]
        small_leg(Moyenne.legend(m,m_keys))
        Desktop.plot_universe(0)
        Desktop.plot_universe(1)
        Desktop.draw()    

Desktop.show()

