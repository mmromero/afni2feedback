import plotter
import pylab as plb

class TimelinePlotter(plotter.Plotter):

  def __init__(self, options):
    plotter.Plotter.__init__(self, options)
    self.NpointsB = 7
    self.NpointsA = 3
    

  def draw(self, values):
    vlen = len(values)
    if vlen == self.nrois:
        
      # Increase the xValues to control the plot
      if len(self.xValues) == 0:
        self.xValues.append(0)
      else:
        self.xValues.append(self.xValues[-1] + 1)            
        
      self.yValues.append(values)
      
      # Transponse the y values matrix for an easy plot
      yvt = zip(*self.yValues)
    
      if len(self.yValues)-self.NpointsB < 0:
          CurrentXAxis=plb.arange(0 ,len(self.yValues))
          for i in plb.arange(0,self.nrois,1):
            self.lines[i].set_data(CurrentXAxis,yvt[i])
        
          self.ax.axis([0, self.NpointsB + self.NpointsA, self.ymin, self.ymax])
      else:
          CurrentXAxis=plb.arange(len(self.yValues)-self.NpointsB, len(self.yValues),1)
          for i in plb.arange(0,self.nrois,1):
            self.lines[i].set_data(CurrentXAxis,yvt[i][-self.NpointsB:])
    
          self.ax.axis([CurrentXAxis.min(), CurrentXAxis.max() + self.NpointsA, self.ymin, self.ymax])
          
      if self.isThresholdDef:
        self.hline = self.ax.axhline(y=self.threshold, color='w', linestyle='--', linewidth=1)
              
    else:
       print("Invalid inpunt values")
          