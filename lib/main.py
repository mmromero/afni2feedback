#!/usr/bin/env python

# ----------------------------------------------------------------------
# This module holds:
#
# main: Initialise afni socket communication and matplotlib figures
#
# ----------------------------------------------------------------------

import numpy as np
from afnicomm import socketcomm as SC

#TODO this will be removed when accepting command line args
port = 53214
debug = 3
graphstyle = 'timeline'


#TODO move to a better place
GRAPH_TL = 'timeline'
GRAPH_BR = 'bar'

# Get an AFNI realtime connection object
comm = SC.AfniRt(port,debug)

# Open the socket
if comm.open_incoming_socket():
    print "error openning socket %s" % port
    print "closing port"
    comm.close_data_ports()
    
if graph == 'timeline'

# Iterate to get new incoming values and plot them.
while 1:
  
  # Wait for new data
  if comm.wait_for_new_run():
      print "error waiting for new run"
      print "closing port"
      comm.close_data_ports()
  
  # Read new data
  if comm.read_all_socket_data():
      print "error reading data"
      print "closing port"
      comm.close_data_ports()
    
  rois_num = comm.get_rois_number()
  if debug > 1:
      print "Received %d rois" % rois_num
    
  rois_val = comm.get_rois_values()
  if debug > 1:
      print "Values: %f" % rois_val
  
  

