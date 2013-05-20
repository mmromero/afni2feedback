import matplotlib as mpl
import matplotlib.pyplot as plt

#TODO move to a configuration file
mpl.rcParams['toolbar'] = 'None'
mpl.rcParams['axes.grid'] = 'False'

def __init__(self):
  self.threshold = 0
  self.isThresholdDef = 0
  self.verbose = 0
  plt.ion()
  plt.show()
  plt.gca().axes.get_xaxis().set_visible(False)
  plt.gca().axes.get_yaxis().set_visible(False)

def set_verbose(self,verbose)
  """ Defines the verbose level """
  self.verbose = verbose
  
def set_threshold(self, threshold):
  """ sets the threshold """
  self.threshold = threshold
  self.isThresholdDef = 1
  
def draw_new_values(self, values):
  """ draw in the next position the set of values passed by argument """
  vlen = len(values)
  if vlen:
      
  else:
      print "No values to plot"