from gui import plotter

class BarPlotter(plotter.Plotter):
  
  def __init__(self, plt, verb):
    plotter.Plotter.__init__(self,plt, verb)
    
  def draw_new_values(self, values):
    """ draw in the next position the set of values passed by argument """
    vlen = len(values)
    if vlen:
	x = range(vlen)
	self.plt.bar(x,values)
    else:
	print "No values to plot"
