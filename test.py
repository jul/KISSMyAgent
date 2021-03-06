#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from utils.matrix import matrix
from utils.agent import BoyScout, ToutPourMaGueule,MetaAgent
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
### même chose comme un tableau lineaire
table=[ 0, -1, 2, 45 ]
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
        print table
        for x,y,value in little:
            m.set(x,y,value)
        self.assertEqual(m.as_table(), table)

class TestAgent(unittest.TestCase):
    buyer=None
    seller= None
    richer_s=None
    richer_b=None

    tpmg=None
    richer_args=dict( 
               utility=100,
               added_value_for_seller=11,
               added_value_for_buyer=1,
               can_bankrupt=False,
               amount_per_transaction=10 ,
               to_debug=True)
    args=dict( 
               utility=100,
               added_value_for_seller=0,
               added_value_for_buyer=0,
               can_bankrupt=False,
               amount_per_transaction=10 ,
               to_debug=True)
    def setUp(self):
        
        self.buyer=BoyScout(x=1,y=1,**self.args)
        self.seller=BoyScout(x=1,y=0,**self.args)
        self.buyer.neighbors= [ self.seller ]
        self.seller.neighbors= [ self.buyer ]
        self.tpmg=ToutPourMaGueule(x=0,y=0,**self.args)
        self.richer_b=BoyScout(x=2,y=2,**self.richer_args)
        self.richer_s=BoyScout(x=2,y=3,**self.richer_args)
        self.richer_s.neighbors=[ self.richer_b ]
        self.richer_b.neighbors=[ self.richer_s ]

        self.tpmg.neighbors = [ self.buyer ]

    def test_getting_richer(self):
        """Condition in which wealth grow + discount"""
        print "RICH"
        self.richer_s.interaction()
        self.assertEqual(self.richer_s.utility,111)
        self.assertEqual(self.richer_b.utility,91)
        print "ERICH"

    def test_simple_transac(self):
        " test simple transfer (no utility added) && color"
        print "ST\n"
        MetaAgent.max_utility=0
        self.seller.interaction()
        self.assertEqual(self.seller.utility,100)
        self.assertEqual(self.buyer.utility,90)
        self.assertEqual(MetaAgent.max_utility,100)
        self.assertEqual(self.seller.color(),"#0000ff")
        MetaAgent.min_utility=-100
        for i in range(-100,101,10):
            self.buyer.utility=i
            expected_color="#00%02xff" %  (  0xff - int(1.0 * ( i +100) / 200 * 255))
            print "buyer utility : %03d -> %s" % ( i,expected_color )

            self.assertEqual(self.buyer.color(),expected_color)
            

        print "\n"

        
    def test_tpmg_transac(self):
        print "\n"
        self.buyer.neighbors= [ self.tpmg ]
        self.tpmg.interaction()
        self.assertEqual(self.tpmg.utility,100)
        self.assertEqual(self.buyer.utility,100)
        self.buyer.interaction()
        self.assertEqual(self.tpmg.utility,110)
        self.assertEqual(self.buyer.utility,90)
        print "\n"

        
    def test_bankrupt_off(self):
        """Test sans banqueroute"""
        print "TB\n"
        self.buyer.can_bankrupt=False
        self.tpmg.can_bankrupt=False
        self.buyer.neighbors= [ self.tpmg ]
        self.buyer.utility=0
        self.tpmg.interaction()
        self.assertEqual(self.tpmg.utility,100)
        self.assertEqual(self.buyer.utility,0)
        self.buyer.interaction()
        self.assertEqual(self.tpmg.utility,110)
        self.assertEqual(self.buyer.utility,-10)
        print "\n"


    def test_bankrupt_on(self):
        """Test avec banqueroute"""
        print "FB\n"
        self.buyer.can_bankrupt=True
        self.tpmg.can_bankrupt=True
        self.buyer.neighbors= [ self.tpmg ]
        self.buyer.utility=0
        self.tpmg.interaction()
        self.assertEqual(self.tpmg.utility,100)
        self.assertEqual(self.buyer.utility,0)
        self.buyer.interaction()
        self.assertEqual(self.tpmg.utility,100)
        self.assertEqual(self.buyer.utility,0)
        print "\n"

    def test_va(self):
        """Valeur ajoutée"""
        print "VA\n"
        self.buyer.added_value_for_seller=7
        self.buyer.added_value_for_buyer=5
        self.seller.added_value_for_seller=10
        self.seller.added_value_buyer=5
        # je donne 10 pour récupérer 10 +  10 
        self.seller.interaction()
        self.assertEqual(self.seller.utility,107)
        # je perd 10 et  écupérer 5
        self.assertEqual(self.buyer.utility,95)
        self.seller.neighbors= [ self.tpmg ]
        self.seller.utility = 100
        self.seller.interaction()
        self.assertEqual(self.tpmg.utility,110)
        self.assertEqual(self.seller.utility,90)
        print "EVA\n"

if __name__ == '__main__':
    unittest.main()
