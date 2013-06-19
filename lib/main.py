#!/usr/bin/env python

# ----------------------------------------------------------------------
# This module holds:
#
# main: Initialise afni socket communication and matplotlib figures
#
# ----------------------------------------------------------------------

import matplotlib
matplotlib.use("GTKAgg")
#TODO move to a configuration file
matplotlib.rcParams['toolbar'] = 'None'

from afnicomm import socketcomm as sc
from gui import barplot as bp
from gui import timelineplot as tlp
import numpy as np
import thread
from optparse import OptionParser


GRAPH_TL = 'timeline'
GRAPH_BR = 'bar'
ERROR = 1
SUCCESS = 0

# -------------------------- UTILS FUNCTIONS --------------------------------#

def log(verbose, text):
    if verbose > 1:
        print("%s" % text)


        
def parse_options():
    """
    Parse the input arguments
    """
    parser = OptionParser()
    
    parser.add_option("-p", "--plot", dest="plot", type="string", \
                      default="bar", action="store",
                      help=" \"bar\" | \"timeline\". Set the plot type." )
                      
    parser.add_option("-d", "--debug", dest="debug", type="int", 
                      default=1, 
                      help=" From 1 to 3 defines de debugging level." )     
                      
    parser.add_option("-t", "--threshold", dest="threshold", type="float",
                      action="store", 
                      help="Set the threshold value as a \n\
                      percentage over the mean ROI value for the N first \n\
                      values received. It must be a value beetween 0 and 4.\n\
                      See --tr-mean option.")

    parser.add_option("-r", "--record", action="store_true", dest="record",
                      default=False, 
                      help="If present it records a mpg4 video \
                      of the experiment.")
                      


    parser.add_option("-m", "--trs-mean", action="store", 
                      dest="trs_mean", type="int", default=3, 
                      help="Set the number of first received ROI values \n\
                      taken into account to calculate the average value. Y \n\
                      span and threshold are based on this mean.")                      
                      
    parser.add_option("-o", "--port", action="store", dest="port", 
                      default=53214, type="int", 
                      help="Socket port number. Defualt value is 53214")
                      
    parser.add_option("-l", "--log", action="store_true", dest="log",
                      default=False, 
                      help="If present the program keeps a log file of the \n\
                      ROI values received.")     
                      
    options, args = parser.parse_args()
    
    return options

# ----------------------------- MAIN CLASS ----------------------------------#

class Neurofeedback:

    def __init__(self, afniComm, options):
        # Get an AFNI realtime connection object
        self.comm = afniComm
        self.options = options        
    
    def process_run (self):
                   # Show restin state image
            self.graph.set_rest_values()
            self.graph.start_rest()
    
            # Wait for new data
            if self.comm.wait_for_new_run():
              log(options.debug, "error waiting for new run\nclosing port")
              self.comm.close_data_ports()
              return ERROR
    
              
    
            # Initialise the average variable
            trs_average = 0
              
    
            # Iterate first TRs
            for i in np.arange(self.options.trs_mean):
    
                # Read new data
                if self.comm.read_TR_data():
                  log(options.debug, "error reading data\nclosing port")
                  self.comm.close_data_ports()
                  return ERROR
    
            # Use the first values to calculate the Y range and threshold
            # level. Then plot.
            rois_values = self.comm.get_rois_values()
            print(rois_values)
            
    
            rois_sum = sum(sum(float(el) for el in els) for els in rois_values)
            trs_average = rois_sum / (self.options.trs_mean * 
                                      self.comm.get_rois_number())
    
            if self.options.threshold:
                self.graph.set_threshold(trs_average *
                                        (1 + self.options.threshold/100))
                
            self.graph.set_run_values(self.comm.get_rois_number(), 
                                      [trs_average*0.97, trs_average*1.07])
            self.graph.start_run()
            
            while not self.comm.read_TR_data(): 
                pass
        
    def iterate_for_runs(self):
        while 1:
            self.process_run()            
            
        self.comm.close_data_ports()         
                 
        return SUCCESS    
        

    def run(self):

        # Open the socket
        if self.comm.open_incoming_socket():
          log(options.debug, "error openning socket %s\n closing port" % \
          self.options.port)
          self.comm.close_data_ports()
          return ERROR          

        # Start the self.graphical area
        if self.options.plot == GRAPH_BR:
            log(options.debug, "starting bar plot...")
            self.graph = bp.BarPlotter(self.options)
        elif self.options.plot == GRAPH_TL:
            log(options.debug, "starting timeline plot...")
            self.graph = tlp.TimelinePlotter(self.options)
        else:
            print "Unknown graph style %s" %self.options.plot
            
        # Start listening from data    
        thread.start_new_thread (self.iterate_for_runs, ())
        
        # Show image from main thread
        self.graph.show(self.comm.get_last_values)


       
# ------------------------------- MAIN --------------------------------------#    

if __name__ == "__main__":
    options = parse_options()
    comm = sc.AfniRt(options)
    nfb = Neurofeedback(comm,options)
    nfb.run()
