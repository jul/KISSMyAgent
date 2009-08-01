#!/usr/bin/python
#_*_ unicode _*_

class Agent:
    _state=None 
    x=None
    y=None
    repres=None
    def __repr__(self):
        return "<repres : %d,%d,%s>" % (x,y,repres)
    def y(self,*y):
        if y!=None:
            self.y=y
        else:
            return self.y

    def x(self,*x):
        if x!=None:
            self.x=x
        else:
            return self.x
    def coord(self,x=None,y=None):
        if (x != None and y != None):
            return (x,y)
        else:
            self.x=x
            self.y=y

    def plot(self):
        color=self.state and "red" or "green"
        self.repres.dot(self.x,self.y,color)

    def __init__(self,**settings):
        print "init\n"
        for k in settings.keys():
            setattr(self,k,settings[k])
            print "%s->%s" % (k,settings[k])
       

    def __str__(self):
        msg=u""

        if self._state:
            msg+="%d,%d//state:%s\n" %  (self.x, self.y, str(self._state))
        return msg

    def state(self,*state):
        if state!=None:
            self._state=state
        else:
            return self._state

    neighbors=[]
    def neighbors(self,nghb=[]):
        if len(nghb):
            self.neighbors=nghb
        else:
            return self.neighbors

	    
