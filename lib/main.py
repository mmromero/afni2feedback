#!/usr/bin/env python

# ----------------------------------------------------------------------
# This module holds:
#
# main: Initialise afni socket communication and matplotlib figures
#
# ----------------------------------------------------------------------
import sys
import numpy as np
from afnicomm import socketcomm as sc
import matplotlib.pyplot as plt

#TODO this will be removed when accepting command line args
port = 53214
debug = 3
graphstyle = 'timeline'


#TODO move to a better place
GRAPH_TL = 'timeline'
GRAPH_BR = 'bar'
ERROR = 1
SUCCESS = 0

class Neurofeedback:

    def __init__(self, afniComm, plt, verb = 1):
      # Get an AFNI realtime connection object
      self.comm = afniComm
      self.verbose = verb
      self.plt = plt

    def run(self):

      # Open the socket
      if self.comm.open_incoming_socket():
          print "error openning socket %s" % port
          print "closing port"
          self.comm.close_data_ports()
          return ERROR
          

      # Iterate to get new incoming values and plot them.
      while 1:
        
        # Wait for new data
        if self.comm.wait_for_new_run():
          print "error waiting for new run"
          print "closing port"
          self.comm.close_data_ports()
          return ERROR
        
        # Read new data
        if self.comm.read_all_socket_data():
          print "error reading data"
          print "closing port"
          self.comm.close_data_ports()
          return ERROR

      return SUCCESS    
    
  
  
if __name__ == "__main__":
    comm = sc.AfniRt(port,debug)
    nfb = Neurofeedback(comm, plt)
    nfb.run()
