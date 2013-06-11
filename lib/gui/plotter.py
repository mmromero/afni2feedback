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
    self.fig = plt.figure()
    self.fig.patch.set_facecolor('black')
    self.ax = self.fig.add_subplot(111)
    self.ax.set_axis_bgcolor('black')
#    self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)
    self.anim = None
    self.lines = None

    
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
    
  def reset_axes(self):
    # if lines remove them
    if self.lines:
        for line in self.lines:
            line.remove()
    
    self.lines = None
      
    # Clear the axes
    self.ax.cla()


  def rest_values(self):
      yield []
   
  def startRest(self, message=None):

    print "Starting RESTING state animation"

    #stop previous animation if any
    if self.anim:
          self.anim._stop()
    
    # stop previous animation if any and clear axes
    self.reset_axes()
    
    self.lines = self.ax.plot([0],[0])
    
    self.ax.relim()
    
    plt.draw()
    
#    self.ax.canvas.restore_region(self.background)
#    
#    self.fig.canvas.blit(self.ax.bbox)
    
#    if self.anim:
#        self.ax.redraw_in_frame()
#    
#    self.anim = anim.ArtistAnimation(self.fig, self.rest_values())
        
    
  def startRun(self, nrois, lims, values_func, num_trs_func):
      
      
    print "Starting RUN animation"
    # stop previous animation if any and clear axes
    self.reset_axes()

    
#    self.fig.canvas.draw_idle()

    self.ymin = lims[0]
    self.ymax = lims[1]       

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

#    self.ax.redraw_in_frame()

    self.ax.relim()
    
#    if not self.anim:
    self.anim = anim.FuncAnimation(self.fig, self.update, values_func, interval=100)
#    else:
#      self.anim._start()
      
    plt.draw()

  def show(self):
    plt.show()
      
     
  
