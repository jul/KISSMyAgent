#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils.matrix import matrix
from utils.agent import *
import numpy as np

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

