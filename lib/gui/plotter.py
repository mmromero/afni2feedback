from matplotlib import pyplot as plt
from matplotlib import animation as anim
import time
import gc

class Plotter:

  def __init__(self, options):
    self.threshold = 0
    self.isThresholdDef = 0
    self.verbose = options.debug
    self.record = options.record
    self.nrois = 0
    self.ymin = 0
    self.ymax = 0
    self.xValues = []
    self.yValues = []
    self.fig = plt.figure()
    self.fig.patch.set_facecolor('black')
    self.ax = self.fig.add_subplot(111)
    self.ax.set_axis_bgcolor('black')
    self.anim = None
    self.lines = []
    self.status = 'Cleared'
    self.hline = None

    
  def set_threshold(self, threshold):
    """ sets the threshold """
    self.threshold = threshold
    self.isThresholdDef = 1
    
    if self.verbose > 2:print "New threshold: %f" %threshold   
    
  def clean_threshold(self):
    if self.isThresholdDef and self.hline:
        self.hline.remove()
        self.hline = None

  def update(self, tr_values):
    """ draw in the next position the set of values passed by argument """

    if self.status == 'Act' or self.status == 'Rest':

        values = tr_values.rois
        num_trs = tr_values.tr_number    
        
        if self.verbose > 2:print "ROI values: ", values
        if self.verbose > 2:print "TR number: ", num_trs
        
        if len(self.xValues) > 0:
          if self.xValues[-1] < num_trs:
            self.draw(values)
          else:
            pass            
        else:
          self.draw(values)
   
    else:
        self.clean_threshold()
        
        if self.lines:
            for line in self.lines:
                line.remove()
            self.lines = None
            self.ax.cla()
            gc.collect()
            
        self.xValues = []
        self.yValues = []
        self.ymin = 0
        self.ymax = 0
        self.threshold = 0
        self.isThresholdDef = 0
    
    return self.lines

  def clear_plot(self):
      
      
    if self.verbose > 0:print "\n++ Plot cleared."
    
    self.status = 'Cleared'
  
  
  def start_resting(self):

    if self.verbose > 0:print "\n++ Starting RESTING period"

    self.fig.patch.set_facecolor('black')
    self.ax.set_axis_bgcolor('black')
                
    self.status = 'Rest'


  def start_activation(self):

    if self.verbose > 0:print "\n++ Starting ACTIVATION period"
    
    self.fig.patch.set_facecolor('white')
    self.ax.set_axis_bgcolor('white')
    
    self.status = 'Act'        
    
    
  def get_line_color(self):
      if self.status == 'Rest':
          return 'white'
      else:
          return 'black'
    
  def set_run_values(self, nrois, lims):
      
    if self.verbose > 1:print "Setting run values..."

    self.ymin = lims[0]
    self.ymax = lims[1]   

    if self.verbose > 2:print "New Y limits: " + ", ".join(map(str,lims))  

    self.nrois = nrois

    if self.nrois == 1:
      self.lines = self.ax.plot([],[], color="white", linestyle='-', linewidth=2)
    elif self.nrois == 2:
      self.lines = self.ax.plot([],[],[],[], color="white", linestyle='-', linewidth=2)
    elif self.nrois == 3:
      self.lines = self.ax.plot([],[],[],[],[],[], color="white", linestyle='-', linewidth=2)
    elif self.nrois == 4:
      self.lines = self.ax.plot([],[],[],[],[],[],[],[], color="white", linestyle='-', linewidth=2)
    elif self.nrois == 5:
      self.lines = self.ax.plot([],[],[],[],[],[],[],[],[],[], color="white", linestyle='-', linewidth=2)
    else:
      if self.verbose > 1:print ("Invalid number of ROIs: %d" % nrois)
      raise AttributeError('The number of rois must be a value between 1 and 5, both included.') 


  def show(self, fargs):
    self.anim = anim.FuncAnimation(self.fig, self.update, fargs, interval=100)

    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    if self.record:
        movie_name = 'run_%s.mp4' %time.time()
        if self.verbose > 2: print 'Recording experiment in %s ...' %movie_name
        self.anim.save(movie_name, fps=25)#, extra_args=['-vcodec', 'libx264'])    
        
    plt.show()
      
     
  
