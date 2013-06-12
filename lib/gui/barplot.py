from gui import plotter
from matplotlib import pylab as plb

class BarPlotter(plotter.Plotter):
  
  def __init__(self, trs_to_mean, verb):
    plotter.Plotter.__init__(self, trs_to_mean, verb)
    
  def draw(self, values):
    """ draw in the next position the set of values passed by argument """
    
    vlen = len(values)
    if vlen == self.nrois:

      # Increase the xValues to control the plot
      if len(self.xValues) == 0:
        self.xValues.append(0)
      else:
        self.xValues.append(self.xValues[-1] + 1)        
        
      x = plb.arange(vlen)
      self.ax.cla()
      self.ax.axis([x[0]-0.8, x[-1]+0.8, self.ymin, self.ymax])
      
      self.lines = self.ax.bar(x,values,width=0.8,bottom=0,align='center')
      
      if self.isThresholdDef:
        self.hline = self.ax.axhline(y=self.threshold)

    else:
	print "No values to plot"