# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 14:22:59 2013

@author: mmolina
"""

import matplotlib
matplotlib.use("GTKAgg")
matplotlib.rcParams['toolbar'] = 'None'
import threading
import time

from matplotlib import pyplot as plt

#from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#import gtk

class AxBuilder (threading.Thread):
    def __init__(self, ax):
        threading.Thread.__init__(self)
        self.ax = ax
        self.cid = ax.figure.canvas.mpl_connect('draw_event', self)

    def run(self):

        print 'Starting graph for the first time...'  
        time.sleep(5)     
        self.lines = self.ax.plot([0],[0])
        
        x = [0]
        y = [0]
        
        while 1:

            print 'Updating axes... x=%d, y=%d' % (x[-1], y[-1])   
        
            self.lines[0].set_data(x,y)
#            self.lines[1].set_data(x*2, y*2)
            self.ax.figure.canvas.draw()
#            self.lines[1].figure.canvas.draw()
            
            x.append(x[-1] + 1)
            y.append(y[-1] + 1)
            
            self.ax.axis([x[1], x[-1], y[1], y[-1]])
            
            time.sleep(1)
            
    def __call__(self, event):
        print "lines draw: " , event

fig = plt.figure()
ax = fig.add_subplot(111)


axbuilder = AxBuilder(ax)

axbuilder.start()

#win = gtk.Window()
#win.add(FigureCanvas(fig))
#win.show_all()
#win.fullscreen()
#line.figure.canvas.show()
#gtk.main()
plt.show()