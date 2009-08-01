from matplotlib import pylab as plt

class Representation:
    step = 1
    color="red"
    canvas=None
    def __init__(self,**settings):
        for k in settings.keys():
            setattr(self,k,settings[k])
        self.canvas=plt

    def dot(self, x, y, color):
        d=self.step - .1 * self.step
        self.canvas.fill( 
            [ x,    x,      x + d,  x + d],
            [ y ,   y + d,  y + d,  y ],
            color if color else self.color
            )
    def show(self):
        self.canvas.show()

def test_repr():
    r=Representation(  step=1, color ="green"  )
    for i in range(0,10):
        for j in range(0, 10):
            r.dot(i,j, "#%d0%d0FF" % (i, j) )
    r.show()
#test_repr()
