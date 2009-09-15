from matplotlib import pylab as plt
from matplotlib import figure

class Representation:
    step = 1
    color="red"
    canvas=None
    graph=None
    plt=None
    draw_x=15
    draw_y=10
    def __init__(self,**settings):
        plt.ion()

        for k in settings.keys():
            setattr(self,k,settings[k])
        fig=plt.figure(figsize=(self.draw_x,self.draw_y))
        self.canvas=fig.add_subplot(1,2,1)
        self.graph=fig.add_subplot(1,2,2)
        # force interactive
        self.plt=plt

    def dot(self, x, y, color):
        d=self.step - .1 * self.step
        self.canvas.fill( 
            [ x,    x,      x + d,  x + d],
            [ y ,   y + d,  y + d,  y ],
            color if color else self.color
            )

    def draw(self):
        self.plt.draw()
        self.canvas.draw()

    def show(self):
        self.plt.show()
def test_repr():
    r=Representation(  step=1, color ="green"   )
    for i in range(0,10):
        for j in range(0, 10):
            r.dot(i,j, "#%d0%d0FF" % (i, j) )
    r.show()
test_repr()
