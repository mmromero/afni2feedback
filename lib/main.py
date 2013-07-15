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
                      
    parser.add_option("-n", "--number-volumes", action="store", 
                      dest="numvols", type="int",
                      help="Set the number of volumes scanned during a \n\
                      resting period. Activation period is assumed to have\n\
                      the same number of volumes.")                      
                      
    parser.add_option("-o", "--port", action="store", dest="port", 
                      default=53214, type="int", 
                      help="Socket port number. Defualt value is 53214")
                      
    parser.add_option("-l", "--log", action="store_true", dest="log",
                      default=False, 
                      help="If present the program keeps a log file of the \n\
                      ROI values received.")     
                      
    options, args = parser.parse_args()
    
    if not options.numvols:
        parser.error("Number of volumes for resting and activations period\n\
        is a required argument. See -n option in --help.")
        parser.exit(ERROR)
    
    return options

# ----------------------------- MAIN CLASS ----------------------------------#

class Neurofeedback:

    def __init__(self, afniComm, options):
        # Get an AFNI realtime connection object
        self.comm = afniComm
        self.options = options        
    
    def process_run (self):

        self.graph.clear_plot()

        # Wait for new data
        if self.comm.wait_for_new_run():
            if self.options.debug > 1: print "error waiting for new run\nclosing port"
            self.comm.close_data_ports()
            return ERROR

        # Firts block is a resting block
        for i in np.arange(self.options.numvols): 
            self.comm.read_TR_data()

        if self.options.debug > 2: 
                print "resting rois: " + ",".join(map(str,self.comm.get_rois_values()))        
        
        # Recalculate baseline
        rois_sum = sum(sum(float(el) for el in els) for els in self.comm.get_rois_values())
        baseline = rois_sum / (self.options.numvols * 
                                  self.comm.get_rois_number())
                                  
            
        if self.options.threshold:
            self.graph.set_threshold(baseline *
                                    (1 + self.options.threshold/100))
            
        self.graph.set_run_values(self.comm.get_rois_number(), 
                                  [baseline*0.97, baseline*1.07])

        strbaseline = '## baseline: %f \n' % baseline
        self.comm.write_log(strbaseline)
        
        resting_roi_values = []

        while 1:
            
            # Start plotting
            self.graph.start_resting()            
            
            # If it is resting period store the values reived
            while not self.comm.read_TR_data() and self.comm.is_resting_period():
                #Store latest values
                resting_roi_values.append(
                self.comm.get_last_roi_values(self.comm.get_rois_values()))            
            
            if self.comm.is_closed():
                self.graph.clear_plot()
                return
            
            if self.options.debug > 2: 
                print "resting rois: " + ",".join(map(str,resting_roi_values))
            
            # Recalculate baseline
            rois_sum = sum(sum(float(el) for el in els) for els in resting_roi_values)
            baseline = rois_sum / (self.options.numvols * 
                                      self.comm.get_rois_number())
            
            strbaseline = '## baseline: %f \n' % baseline
            self.comm.write_log(strbaseline)
            
            if self.options.threshold:
                self.graph.set_threshold(baseline *
                                        (1 + self.options.threshold/100))
                
            self.graph.set_run_values(self.comm.get_rois_number(), 
                                      [baseline*0.97, baseline*1.07])
    

            # Start plotting
            self.graph.start_activation()            
            
            # If activation pariod read values
            while not self.comm.read_TR_data() and not self.comm.is_resting_period():
                pass

            if self.comm.is_closed():
                self.graph.clear_plot()
                return               
            
            # Restart the last rois values vector and append the first 
            # resting value
            resting_roi_values = []
            resting_roi_values.append(
                self.comm.get_last_roi_values(self.comm.get_rois_values()))
            
        

    def run(self):

        # Open the socket
        if self.comm.open_incoming_socket():
          if self.options.debug > 1: 
             print  "error openning socket %s\n closing port" % self.options.port
          self.comm.close_data_ports()
          return ERROR          

        # Start the self.graphical area
        if self.options.plot == GRAPH_BR:
            if self.options.debug > 1: print  "starting bar plot..."
            self.graph = bp.BarPlotter(self.options)
        elif self.options.plot == GRAPH_TL:
            if self.options.debug > 1: print "starting timeline plot..."
            self.graph = tlp.TimelinePlotter(self.options)
        else:
            print "Unknown graph style %s" %self.options.plot
            
        # Start listening from data    
        thread.start_new_thread (self.process_run, ())
        
        # Show image from main thread
        self.graph.show(self.comm.get_last_values)


       
# ------------------------------- MAIN --------------------------------------#    

if __name__ == "__main__":
    options = parse_options()
    comm = sc.AfniRt(options)
    nfb = Neurofeedback(comm,options)
    nfb.run()
