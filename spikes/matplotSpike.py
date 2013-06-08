import time
import os
import numpy as np
import matplotlib as mpl
mpl.use('GTKAgg')

import matplotlib.pyplot as plt
import pylab as plb

mpl.rcParams['toolbar'] = 'None'
mpl.rcParams['axes.grid'] = 'False'

screen = os.popen("xrandr | grep '*' | awk '{print $1}'").readlines()[0]
w ,h = screen.rsplit("x")
dpi = 80

fig=plt.figure(figsize=(int(w)/dpi,int(h)/dpi))
fig.set_frameon(True)

i=0
x=list()
y=list()

plt.ion()
plt.show()
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)

ax0= plt.subplot(211)
ax = plt.subplot(212)

line1=ax.plot([], [],[],[])


while i <50:
    temp_y=np.random.random()
    x.append(i)
    y.append(temp_y)
    plt.subplot(211)
    plt.bar(i,temp_y)
    plt.axhline(y=0.5)
    plt.box('off')
    plt.hold(False)
    
    plt.subplot(212)

    CurrentXAxis=plb.arange(len(y)-4,len(y),1)
    line1[0].set_data(CurrentXAxis,plb.array(y[-4:]))
    line1[1].set_data(CurrentXAxis,plb.array(y[-4:])*2)
    ax.set_xlim((CurrentXAxis.min(),CurrentXAxis.max()+2))
    ax.set_ylim(-1.5,1.5)
    plt.axhline(y=0.5)
    
    i+=1
    plt.draw()
    time.sleep(1)
