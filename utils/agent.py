#i!/usr/bin/python
#_*_ unicode _*_



    
class MetaAgent:
    stat=None 
    personality="naive"
    x=None
    to_debug=False
    y=None
    max_id=0
    repres=None
    neighbors=[]
    id=None
    memory=dict()
    transaction_amount=10
    personalities=[]
    max_utility=0
    added_value_per_transaction=5
    pers_color_mask= 0x0000FF
    
    def __repr__(self):
        return "<repres : %d,%d,%s>" % (self.x,self.y,self.repres)
    def coord(self,x=None,y=None):
        if (x != None and y != None):
            return (x,y)
        else:
            self.x=x
            self.y=y

    def plot(self):
        self.debug("%d , %d " % (self.utility, self.max_utility) )
        color = (
                 ( 0xff - int (   (  1.0 * 0xff  *  self.utility / self.max_utility) ) ) << 8 & 0x00ff00
                 |  self.pers_color_mask
                ) 
            
        self.debug( " color : #%06x\n" % color)
        self.repres.dot(self.x,self.y, "#%06x" % color)

    def __init__(self,**settings):
        MetaAgent.max_id=MetaAgent.max_id+1
        self.id=MetaAgent.max_id
        for k in settings.keys():
            setattr(self,k,settings[k])
            #print "%s->%s" % (k,settings[k])
        MetaAgent.max_utility=max(MetaAgent.max_utility, self.utility)
        if self.personality not in self.personalities:
            self.personalities+=[ self.personality ]
        print "init %s\n" % self
    
    def debug(self,msg=""):
        if self.to_debug:
            msg= "%s(%d,%d) %s :utilisty:%s::%s" % ( 
               self.id, 
               self.x,
               self.y,
               self.personality,
               self.utility,
               msg)
            print msg
    def choose_neighbor(self):
        "choix par defaut=au hasard"
        from random import choice
        return choice(self.neighbors)
    
    def interaction(self):
        
        a_rand_neighbor=self.choose_neighbor()
        ## est ce que l'on veut faire du commerce avec le voisin ?  
        if(a_rand_neighbor == False):
            return False
        self.debug("amount before transaction with %d " % ( a_rand_neighbor.id) )
        ## on retire le montant de la transaction 
        self.utility-=self.transaction_amount
        ### on recupere le montant de la transaction + bonus ....
        ### eventuellement 
        self.utility+=a_rand_neighbor.transaction(self.transaction_amount)
        self.debug("utility after transaction : %d" % self.utility)
        MetaAgent.max_utility=max(MetaAgent.max_utility, self.utility)
        
    def transaction(self,amount):
        ## je prend l'objet 
        self.utility+=amount
        self.debug("transaction made I get %d" % amount)
        ### je prend de mon larre feuille
        ### et je paie
        return self.added_value_per_transaction + amount


    def __str__(self):
        msg=u""

        if self.utility:
            msg+="%d,%d//id=%d//utility:%s//pers:%s\n" %  (self.x, self.y,self.id, str(self.utility),self.personality)
        return msg
class BoyScout(MetaAgent):
    def __init__(self,**kwargs):
        kwargs["personality"]="BoyScout"
        print kwargs
        MetaAgent.__init__(self,**kwargs)

class ToutPourMaGueule(MetaAgent):
    def __init__(self,**kwargs):
        kwargs["personality"]="ToutPourMaGueule"
        kwargs["pers_color_mask"]=0xCC0000
        MetaAgent.__init__(self,**kwargs)

    def choose_neighbor(self):
        self.debug("on fait pas de commerce")
        return False

    def transaction(self,amount):
        self.utility+=amount
        MetaAgent.max_utility=max(MetaAgent.max_utility, self.utility)
        self.debug("je prend mais ne rends pas")
        return 0



