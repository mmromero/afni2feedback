from matplotlib import pyplot as plt
from matplotlib import animation as anim

class Plotter:

  def __init__(self, trs_to_mean, verb=1):
    self.threshold = 0
    self.isThresholdDef = 0
    self.verbose = verb
    self.nrois = 0
    self.ymin = 0
    self.ymax = 0
    self.xValues = []
    self.yValues = []
    self.trs_to_mean = trs_to_mean + 1
    
  def set_threshold(self, threshold):
    """ sets the threshold """
    self.threshold = threshold
    self.isThresholdDef = 1

  def update(self, tr_values):
    """ draw in the next position the set of values passed by argument """

    values = tr_values.rois
    num_trs = tr_values.tr_number    
    
    print "ROI values: ", values
    print "TR number: ", num_trs
    
    if len(self.xValues) > 0:
      if self.xValues[-1] < (num_trs - self.trs_to_mean):
        self.draw(values)
      else:
        pass            
    else:
      self.draw(values)

    return self.lines  
    
  def startFigure(self, nrois, lims, values_func, num_trs_func):

    self.ymin = lims[0]
    self.ymax = lims[1]         

    fig = plt.figure()
    self.ax = fig.add_subplot(111)

    self.nrois = nrois
    if self.nrois == 1:
      self.lines = self.ax.plot([],[])
    elif self.nrois == 2:
      self.lines = self.ax.plot([],[],[],[])
    elif self.nrois == 3:
      self.lines = self.ax.plot([],[],[],[],[],[])
    elif self.nrois == 4:
      self.lines = self.ax.plot([],[],[],[],[],[],[],[])
    elif self.nrois == 5:
      self.lines = self.ax.plot([],[],[],[],[],[],[],[],[],[])
    else:
      print ("Invalid number of ROIs: %d" % nrois)
      raise AttributeError('The number of rois must be a value between 1 and 5, both included.') 

    self.anim = anim.FuncAnimation(fig, self.update, values_func, interval=100)
    plt.show()

      
     
  
