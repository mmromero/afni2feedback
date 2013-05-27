import matplotlib as mpl

#TODO move to a configuration file
mpl.rcParams['toolbar'] = 'None'
mpl.rcParams['axes.grid'] = 'False'

class Plotter:

  def __init__(self, plt, verb=1):
    self.threshold = 0
    self.isThresholdDef = 0
    self.verbose = verb
    self.plt = plt
    self.plt.ion()
    self.plt.show()
    self.plt.gca().axes.get_xaxis().set_visible(False)
    self.plt.gca().axes.get_yaxis().set_visible(False)
    
  def set_threshold(self, threshold):
    """ sets the threshold """
    self.threshold = threshold
    self.isThresholdDef = 1
    self.plt.axhline(y=threshold)

  
