# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 08:14:35 2013

@author: mmolina
"""
import matplotlib
matplotlib.use("GTKAgg")
matplotlib.rcParams['toolbar'] = 'None'

from matplotlib import pyplot as plt

#from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#import gtk

class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print 'click', event
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click to build line segments')
line, = ax.plot([0], [0])  # empty line
linebuilder = LineBuilder(line)


#win = gtk.Window()
#win.add(FigureCanvas(fig))
#win.show_all()
#win.fullscreen()
#line.figure.canvas.show()
#gtk.main()
plt.show()


