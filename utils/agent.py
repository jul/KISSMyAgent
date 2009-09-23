#i!/usr/bin/python
#_*_ unicode _*_



    
class MetaAgent:
    stat=None 
    personality="naive"
    x=None
    to_debug=True
    y=None
    max_id=0
    repres=None
    neighbors=[]
    id=None
    memory=dict()
    transaction_amount=10
    personalities=[]
    utility=50
    init_val=dict()
    max_utility=0
    min_utility=0
    can_bankrupt=True
    current_partner=None
    added_value_for_buyer=1
    added_value_for_seller=9
    pers_color_mask= 0x0000FF
    def __repr__(self):
        return "<repres : %d,%d,%s>" % (self.x,self.y,self.repres)
    def coord(self,x=None,y=None):
        if (x == None and y == None):
            return (self.x,self.y)
        else:
            self.x=x
            self.y=y

    def color(self):
        #self.debug("%d , %d " % (self.utility, self.max_utility) )
        assert(self.utility <= MetaAgent.max_utility )
        ratio_to_max= 1.0 * ( self.utility - MetaAgent.min_utility ) / (MetaAgent.max_utility - MetaAgent.min_utility ) 
        color = (
            (
                 ( 0x00ff - 
                   int (   
                    (  ratio_to_max * 0x00ff   ) 
                    ) 
                 ) << 8 & 0x00ff00
            )
            |  self.pers_color_mask
        ) 
        #self.debug( " color : #%06x\n" % color)
        return( "#%06x" % color)

    def clone(self,**change):
        arg=dict()
        for k in self.init_val.keys():
            arg[k]=self.init_val[k]
        for k in change.keys():
            arg[k]=change[k]
        self.debug("avant")

        c=self.__class__(**arg)
        c.debug("apres")
        return c

    def __init__(self,**settings):
        MetaAgent.max_id=MetaAgent.max_id+1
        self.id=MetaAgent.max_id
        self.init_val=settings
        for k in settings.keys():
            setattr(self,k,settings[k])
            #print "%s->%s" % (k,settings[k])
        MetaAgent.max_utility=max(MetaAgent.max_utility, self.utility)
        MetaAgent.min_utility=min(MetaAgent.min_utility, self.utility)
        if self.personality not in self.personalities:
            self.personalities+=[ self.personality ]
        #print "init %s\n" % self

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
        self.current_partner=choice(self.neighbors)
        return self.current_partner
    def deal_with(self,partner):
        ## est ce que l'on veut faire du commerce avec le voisin ?  
        if( not partner ):
            return amount
        self.debug("amount before transaction with %d " % ( partner.id) )
        ## on retire le montant de la transaction 
        self.utility-=self.transaction_amount
        ### on recupere le montant de la transaction + bonus ....
        ### eventuellement 
        self.utility+=partner.transaction(self.transaction_amount)
        self.debug("utility after transaction : %d" % self.utility)
        MetaAgent.max_utility=max(MetaAgent.max_utility, self.utility)
        MetaAgent.min_utility=min(MetaAgent.min_utility, self.utility)

    def interaction(self,agent=None):
        if self.can_bankrupt and self.utility <= 0:
            self.current_partner = None
            return False

        self.current_partner = agent if agent else self.choose_neighbor()
        self.deal_with(self.current_partner)
    def transaction(self,amount):
    ### I am the buyer
        if self.can_bankrupt and self.utility <= amount:
            return amount

        self.utility -=  amount 
        self.utility += self.added_value_for_buyer 
        self.debug("transaction made I give %d" %  ( amount + self.added_value_for_seller) )
        ### je prend de mon larre feuille
        ### et je paie
        return self.added_value_for_seller + amount


    def __str__(self):
        msg=u""

        if self.utility:
            msg+="%d,%d//id=%d//utility:%s//pers:%s\n" %  (self.x, self.y,self.id, str(self.utility),self.personality)
        return msg

class ToutPourMaGueule(MetaAgent):
    def __init__(self,**kwargs):
        kwargs["personality"]="ToutPourMaGueule"
        kwargs["pers_color_mask"]=0xCC0000
        self=MetaAgent.__init__(self,**kwargs)


    def choose_neighbor(self):
        self.debug("on fait pas de commerce")
        self.current_partner=None
        return False

    def deal_with(self,agent=None):
        self.debug("Pas de deal")
        return False

    def transaction(self,amount):
        self.utility+=amount
        MetaAgent.max_utility=max(MetaAgent.max_utility, self.utility)
        MetaAgent.min_utility=min(MetaAgent.min_utility, self.utility)
        self.debug("je prend mais ne rends pas")
        return 0

class BoyScout(MetaAgent):
    def __init__(self,**kwargs):
        kwargs["personality"]="Confiant"
        MetaAgent.__init__(self,**kwargs)



