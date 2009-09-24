from matplotlib import pylab as plt
from matplotlib import figure

class Representation:
    step = 1
    color="red"
    canvas=[]
    nb_canvas=1
    nb_graph=1
    universe = []
    graph=[]
    plt=None
    x=20
    fig=None
    y=10
    def __init__(self,**settings):
        plt.ion()

        for k in settings.keys():
            setattr(self,k,settings[k])
        fig=plt.figure(figsize=(self.x,self.y))
        total=self.nb_graph + self.nb_canvas 
        curseur = 1
        for i in range(0,self.nb_canvas):
            self.canvas += [ fig.add_subplot(1,total,curseur) ]
            print " adding one canvas"
            curseur+=1
        for i in range(0,self.nb_graph):
            self.graph += [ fig.add_subplot(1,total,curseur) ]
            print " adding one graph"
            curseur+=1
        fig.subplots_adjust(bottom=.2)
        # force interactive
        print "total %d " % total
        self.plt=plt
        self.fig=fig

    def plot_universe(self,index=0):
        for ag in self.universe[index].matrix.as_table():
            self.dot(ag.x, ag.y,ag.color(),index)
        if self.universe[index].title:
            self.canvas[index].set_title(self.universe[index].title)



    
    def dot(self, x, y, color,index=0):
        d=self.step - .1 * self.step
        self.canvas[index].fill( 
            [ x,    x,      x + d,  x + d],
            [ y ,   y + d,  y + d,  y ],
            color if color else self.color
            )

    def clear(self):
        for g in self.graph:
            g.clear()

    def draw(self):
        self.plt.draw()

    def show(self):
        self.plt.show()
def test_repr():
    r=Representation(  step=1, color ="green"   )
    for i in range(0,10):
        for j in range(0, 10):
            r.dot(i,j, "#%d0%d0FF" % (i, j) )
    r.show()
if __name__ == '__main__':
    test_repr()
