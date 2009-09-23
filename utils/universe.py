#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils.matrix import matrix
from utils.agent import *
import numpy as np

UP = ( 0,1 )
DOWN= (0,-1)
LEFT= ( 1, 0)
RIGHT = ( -1, 0 ) 
DIRECTIONS= ( UP, DOWN,LEFT, RIGHT )
class Universe:
    "gère le temps et l'espace pour une simulation"
    matrix=None
    size_x=10
    size_y=10
    repres=None
    graph=None
    title=None
    temp=4000
    pct_bs=50
    agent_args=dict()
    current_agent=None
    
        
    def __init__(self,**args):
        from random import randint as rand
        
        for k in args.keys():
            setattr(self,k,args[k])
        x=self.size_x
        y=self.size_y
        self.matrix=matrix(x,y)
        ### init agent
        for i in range(0,x):
            for j in range(0,y):   
                  args=self.agent_args
                  args["x"]=i
                  args["y"]=j

                  self.matrix.set(
                    i,j, 
                    BoyScout(**args) if rand(0,101) <= self.pct_bs  else ToutPourMaGueule(**args)
                 )
        ## init voisinage
        self.set_neighb()

    def set_neighb(self):
        for i in range(0,self.size_x):
            for j in range(0,self.size_y):   
                neigb=[]
                for coord in DIRECTIONS:
                        dx,dy=coord
                        neigb.append(self.matrix.get(
                            (i+dx)%self.size_x,
                            (j+dy)%self.size_y
                            )
                        )

                self.matrix.get(i,j).neighbors=neigb
        
    
    def next(self):
        self.current_agent=self.matrix.get_rand()
        self.current_agent.interaction()
        self.temp-=1 
        return self.temp >= 0

