#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from utils.matrix import matrix
values =  ( 
## x,y, value
(0,0, 1),
(0,1, 2),
(1,3, 3),
(5,7, 4),
## element le plus grand
(6,9,5)
)

little=(
(0,0,0),
(0,1,2),
(1,0,-1),
(1,1,45)
)
class TestMatrix(unittest.TestCase):
    m=None
    def setUp(self):
        self.m=matrix(7,10)
        

    def testlen(self):
        self.assertEqual(len(self.m.as_table()),70,"bonne taille allouee")
    def test_set_get(self):
        "set et get sont ils réversibles ? "
        m=self.m
        for x,y,value in values:
            m.set(x,y,value)
            print "%d,%d=>%d" % (x,y,value)
            self.assertEqual(m.get(x,y),value) 

    def test_as_table(self):
        m=matrix(2,2)
        table=[ 0, -1, 2, 45 ]
        print table
        for x,y,value in little:
            m.set(x,y,value)
        self.assertEqual(m.as_table(), table)

if __name__ == '__main__':
    unittest.main()
