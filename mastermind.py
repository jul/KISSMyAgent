#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils.matrix import matrix
from utils.agent import *
from utils.graph import Representation
from utils.universe import Universe
import numpy as np
import pdb

x=10
y=10
draw_time=200
args=dict( size_x= x, 
           title="Without Bankrupty (wo_b)",
           size_y= y, 
           pct_bs=30,
           agent_args= dict(
               # 1 de VA finales par transaction
               added_value_for_seller=12,
               amount_per_transaction=10,
               added_value_for_buyer=1,
               to_debug=True,
               can_bankrupt=False,
               utility=100,
           ),
           temp= 10000 )
u=Universe(**args)
args["title"]="With Bankrupty (w_b)"
u2=Universe(**args)
args["title"]="Fail before Banrukpt (f_b)"
u3=Universe(**args)

Desktop=Representation(universe=[ u,u2,u3 ],nb_canvas=3,nb_graph=2,x=20,y=12)
Desktop.fig.text(.3,.95,
    "Effect of bankrupty and unsolvability on a world of transactions (%d %% collectors)" % 
    ( 100 - args["pct_bs"] ),
    fontsize=18
)
Moyenne=Desktop.graph[0]
Total=Desktop.graph[1]
#Moyenne_p=Desktop.graph[2]

u2.matrix.matrix = [ 
    a.clone( can_bankrupt = True ) for a in  u.matrix.as_table() 
] 
u3.matrix.matrix = [ 
    a.clone( can_bankrupt = True, fail_before_bankrupcy=True ) for a in  u.matrix.as_table() 
]

u2.set_neighb()

def small_leg(leg):
    for t in leg.get_texts():
        t.set_fontsize('small')

i=0
res=dict()
res_pert=dict()
res_fail=dict()
wealth=dict(
    w_b=[], wo_b= [], f_b=[]
)
perso_count=dict()
for k in MetaAgent.personalities:
    res[k]=[]
    res_pert[k]=[]
    res_fail[k]=[]
    perso_count[k]=0

initial_wealth=0
for agent in u2.matrix.as_table():
    initial_wealth+=agent.utility
    perso_count[agent.personality] += 1
assert(x*y*args["agent_args"]["utility"] == initial_wealth)

Desktop.plot_universe()

while u.next():
    i+=1
    ( x , y ) =  u.current_agent.coord()
    ## mimic on u2
    agent=u2.matrix.get(x,y)
    if (u.current_agent.current_partner) :
        (px, py) =u.matrix.get(x,y).current_partner.coord()
        partner = u2.matrix.get(px,py)
        if partner and  agent.interaction(partner):
            agent.deal_with(partner)
    ## mimic on u3
    agent=u3.matrix.get(x,y)
    if (u.current_agent.current_partner) :
        (px, py) =u.matrix.get(x,y).current_partner.coord()
        partner = u3.matrix.get(px,py)
        if partner and  agent.interaction(partner):
            agent.deal_with(partner)

    res_temp=dict()
    res_temp_pert=dict()
    res_temp_fail=dict()
    for g in wealth.keys():
        wealth[g]+= [ 0 ]
    for k in MetaAgent.personalities:
        res_temp[k]=0
        res_temp_pert[k]=0
        res_temp_fail[k]=0
    for agent in u2.matrix.as_table():
        wealth["w_b"][i-1]+=agent.utility
        res_temp_pert[agent.personality] +=  agent.utility
    
    for agent in u3.matrix.as_table():
        wealth["f_b"][i-1]+=agent.utility
        res_temp_fail[agent.personality] +=  agent.utility
    
    for agent in u.matrix.as_table():
        wealth["wo_b"][i-1]+=agent.utility
        res_temp[agent.personality] +=  agent.utility
    
    for g in wealth.keys():
        wealth[g][ i - 1 ] *= 1.0 /  initial_wealth 
    t=[]
    t_keys=[]
    p=[]
    keys=[]
    m=[]
    m_keys=[]
    for perso in res_temp.keys():
        res[perso] += [ res_temp[perso] ]
        res_pert[perso] += [ res_temp_pert[perso] ]
        res_fail[perso] += [ res_temp_fail[perso] ]

    under_graph=(0,-.25)
    if ( i % draw_time  == 0):

        Desktop.clear()
        Total.set_title("Total utility per  universe")
        Moyenne.set_title("mean utility per perso / universe")
    
        for grid in wealth.keys():
            p += [ Total.plot(wealth[grid] )] 
            keys += [ "ratio of initwealth in %s" % grid ]
        Total.legend(p,keys,loc=under_graph)
        
        m=[]
        m_keys=[]
        for perso in res_temp.keys():

            m += [ 
                Moyenne.plot( 
                    [ r/perso_count[perso] for r in res[perso] ]  ) ,
                Moyenne.plot(
                    [ r/perso_count[perso] for r in res_pert[perso] ]  ),
                Moyenne.plot( 
                    [ r/perso_count[perso] for r in res_fail[perso] ]  )  
            ] 
            m_keys += [ 
                "wo_b : %s (%.2f)" % (
                    perso, 1.0 * res_temp_pert[perso] / perso_count[perso]  
                ), 
                "w_b : %s (%.2f)" % (
                    perso, 1.0 * res_temp[perso] / perso_count[perso]
                ), 
                "f_b : %s (%.2f)" % (
                    perso, 1.0 * res_temp_fail[perso] / perso_count[perso]
                ), 
            ]

        small_leg(Moyenne.legend(m,m_keys,loc=under_graph))
        Moyenne.set_xticks( range(0, i + 1, i>>2 ))
        Total.set_xticks( range(0, i+1, i>>2 ))

        Desktop.plot_universe(0)
        Desktop.plot_universe(1)
        Desktop.plot_universe(2)
        Desktop.draw()    

Desktop.show()

