# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 14:53:22 2013

@author: mmolina
"""

import numpy as np
import matplotlib
matplotlib.use("GTKAgg")
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pylab as plb
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot(111)
line1, line2 = ax.plot(plb.arange(10),np.random.rand(10), plb.arange(10), np.random.rand(10))
ax.set_ylim(0, 1)

def update(arg=None):
    line1.set_ydata(np.random.rand(10))
    line2.set_ydata(np.random.rand(10))
    return line1, line2

#def data_gen():
#    while True: yield np.random.rand(10)

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()