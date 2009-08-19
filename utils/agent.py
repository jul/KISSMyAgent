#!/usr/bin/python
#_*_ unicode _*__

    
class Agent:
    stat=None 
    personality=None
    x=None
    debug=True
    y=None
    max_id=0
    repres=None
    neighbors=[]
    id=None
    memory=dict()
    transaction_amount=10
    max_utility=0
    added_value_per_transaction=0
    pers_color_mask= dict( 
        boy_scout = 0x0000000FF00 ,
        only_take = 0x00000FF0000,
    ) 
    personalities = ( "boy_scout", "only_take" ) 
    
    def __repr__(self):
        return "<repres : %d,%d,%s>" % (self.x,self.y,self.repres)
    def coord(self,x=None,y=None):
        if (x != None and y != None):
            return (x,y)
        else:
            self.x=x
            self.y=y

    def plot(self):
         
        color = (  
                 (
                    0xff -
                    int (   ( 0xff  / Agent.max_utility ) * self.utility) 
                ) 
                |  
             Agent.pers_color_mask[ self.personality ] 
            )
            
        print " color : #%06x\n" % color
        self.repres.dot(self.x,self.y, "#%06x" % color)

    def __init__(self,**settings):
        Agent.max_id=Agent.max_id+1
        self.id=Agent.max_id
        for k in settings.keys():
            setattr(self,k,settings[k])
            #print "%s->%s" % (k,settings[k])
        Agent.max_utility=max(Agent.max_utility, self.utility)
        print "init %s\n" % self
    def has_good_memorie(self):
        return True
    
    def debug(self,msg=""):
        if Agent.debug:
            msg= "%s(%d,%d) %s ::%s" % ( 
               self.id, 
               self.x,
               self.y,
               self.personality,
               msg)
            print msg

    def interaction(self):
        from random import choice
        if not self.has_good_memorie():
            return False
        #if self.personality == "only_take":
        #    self.debug(" on ne fait pas de commerce (pas fou)")
            
         #   return False
        a_rand_neighbor=choice(self.neighbors)
        self.debug("amount before transaction with %d : %d" % ( 
            a_rand_neighbor.id,
            self.utility
            )
            )

        ## on retire le montant de la transaction 
        self.utility-=self.transaction_amount
        ### on recupere le montant de la transaction + bonus ....
        ### eventuellement 
        self.utility+=a_rand_neighbor.transaction(self.transaction_amount)
        self.debug("utility after transaction : %d" % self.utility)
        Agent.max_utility=max(Agent.max_utility, self.utility)
        self.plot()
        
    def transaction(self,amount):
        ## je prend l'objet 
        self.utility+=amount
        self.debug("transaction made I get %d" % amount)
        ### et je retourne le montant  ou pas 
        if self.personality == "only_take":
            # je me casse en courant

            return 0 
        else:
            ### je prend de mon larre feuille
            self.utility-=amount
            ### et je paie
            return self.added_value_per_transaction + amount
        self.plot()


    def __str__(self):
        msg=u""

        if self.utility:
            msg+="%d,%d//id=%d//utility:%s//pers:%s\n" %  (self.x, self.y,self.id, str(self.utility),self.personality)
        return msg

    

	    
