#!/usr/bin/python
#_*_ unicode _*__
behaviour=dict( 
)
    
class Agent:
    stat=None 
    personality=None
    x=None
    y=None
    max_id=0
    repres=None
    neighbors=[]
    id=None
    memory=dict()
    transaction_amount=1
    max_utility=0
    added_value_per_transaction=.1
    pers_color_mask= dict( 
        boy_scout = 0x00FF00 ,
        only_take = 0xFF0000,
   ) 
    
    def __repr__(self):
        return "<repres : %d,%d,%s>" % (x,y,repres)
    def coord(self,x=None,y=None):
        if (x != None and y != None):
            return (x,y)
        else:
            self.x=x
            self.y=y

    def plot(self):
         
        color = int (  0xffffff * (  
                    self.utility / Agent.max_utility 
                   ) 
                ) & Agent.pers_color_mask[ self.personality ]
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

    def interaction(self):
        from random import Random as rand
        if not self.has_good_memorie():
            return False
        
        a_rand_neighbor=self.neighbors[ 
            rand().randint(0,len(self.neighbors) - 1 )
        ]
        ## on retire le montant de la transaction 
        self.utility-=self.transaction_amount
        ### on recupere le montant de la transaction + bonus ....
        ### eventuellement 
        self.transaction+=a_rand_neighbor.transaction(self.transaction_amount)
        Agent.max_utility=max(Agent.max_utility, self.transaction)
        
    def transaction(self,amount):
        if self.personality == "only_take":
            return 0
        else:
            return self.amount.added_value_per_transaction * amount


    def __str__(self):
        msg=u""

        if self.utility:
            msg+="%d,%d//id=%d//utility:%s//pers:%s\n" %  (self.x, self.y,self.id, str(self.utility),self.personality)
        return msg

    

	    
