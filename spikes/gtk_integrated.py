# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 21:40:26 2013

@author: mmolina
"""

import gtk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import pylab as plb
import time
import thread

def gtk_main():
    gtk.main()
    

win = gtk.Window()
win.connect("destroy", lambda x: gtk.main_quit())

plt.ion()
fig =  plt.figure(figsize=(10,8))
plt.close()

ax = fig.add_subplot(111)
lines = ax.plot([1, 2, 3, 4],[1, 2, 3, 4,], [5, 6, 7, 8], [5, 6, 7, 8])
canvas = FigureCanvas(fig)

win.add(canvas)
win.show_all()
win.fullscreen()
plt.draw()

thread.start_new_thread( gtk_main,() )

i = [0]
while 1:
    i.append(i[-1] + 1)
    x = plb.arange(0 ,len(i))
    lines[0].set_data(x,i)
    lines[1].set_data(x,i)
    
    plt.draw()
    time.sleep(1)

