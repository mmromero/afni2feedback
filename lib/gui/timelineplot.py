import plotter

class TimelinePlotter(plotter.Plotter):

  def __init__(self, plt, verb):
    plotter.Plotter.__init__(self,plt, verb)
    
  def draw_new_values(self, values):
    """ draw in the next position the set of values passed by argument """
    vlen = len(values)
    if vlen:
      #TODO
      print "TODO"
    else:
      print "No values to plot"
