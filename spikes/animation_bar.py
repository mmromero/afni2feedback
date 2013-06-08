# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 14:53:22 2013

@author: mmolina
"""

import numpy as np
import matplotlib
matplotlib.use("GTKAgg")
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot(111)
ax.bar([0 ,1],np.random.rand(2))
ax.set_ylim(0, 1)

def update(arg=None):
    ax.cla()
    ax.axhline(y=0.5)
    ax.set_ylim(0, 1)
    return ax.bar([0 ,1],np.random.rand(2))

#def data_gen():
#    while True: yield np.random.rand(10)

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()