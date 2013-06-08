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

#TODO this will be removed when accepting command line args
port = 53214
debug = 3
graphstyle = 'bar'


#TODO move to a better place
GRAPH_TL = 'timeline'
GRAPH_BR = 'bar'
ERROR = 1
SUCCESS = 0

TRS_TO_AVERAGE = 3
# --------------------------

def log(verbose, text):
    if verbose > 1:
        print("%s" % text)
        

class Neurofeedback:

    def __init__(self, afniComm, verb = 1):
        # Get an AFNI realtime connection object
        self.comm = afniComm
        self.verbose = verb

    def read_tr_loop(self):
        while not self.comm.read_TR_data(): 
            pass

    def run(self):

        # Open the socket
        if self.comm.open_incoming_socket():
          log(self.verbose, "error openning socket %s\n closing port" % port)
          self.comm.close_data_ports()
          return ERROR          

        # Wait for new data
        if self.comm.wait_for_new_run():
          log(self.verbose, "error waiting for new run\nclosing port")
          self.comm.close_data_ports()
          return ERROR

        # Start the graphical area
        if graphstyle == GRAPH_BR:
            log(self.verbose, "starting bar plot...")
            graph = bp.BarPlotter( TRS_TO_AVERAGE, self.verbose)
        else:
            log(self.verbose, "starting timeline plot...")
            graph = tlp.TimelinePlotter(TRS_TO_AVERAGE, self.verbose)              

        # Initialise the average variable
        trs_average = 0
          

        # Iterate first TRs
        for i in np.arange(TRS_TO_AVERAGE):

            # Read new data
            if self.comm.read_TR_data():
              log(self.verbose, "error reading data\nclosing port")
              self.comm.close_data_ports()
              return ERROR

        # Use the first values to calculate the Y range and threshold
        # level. Then plot.
        rois_values = self.comm.get_rois_values()
        print(rois_values)
        

        rois_sum = sum(sum(float(el) for el in els) for els in rois_values)
        trs_average = rois_sum / (TRS_TO_AVERAGE * self.comm.get_rois_number())

        graph.set_threshold(trs_average*1.02)
        
        thread.start_new_thread(self.read_tr_loop, ())

        graph.startFigure(self.comm.get_rois_number(), [trs_average*0.97, trs_average*1.07], self.comm.get_last_values, self.comm.get_num_read)


        self.comm.close_data_ports()         
                 
        return SUCCESS    
    

if __name__ == "__main__":
    comm = sc.AfniRt(port,debug)
    nfb = Neurofeedback(comm)
    nfb.run()
