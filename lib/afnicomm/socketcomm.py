#!/usr/bin/env python

# ----------------------------------------------------------------------
# This module holds:
#
# AfniRt: The simplified interface for the RTInterface provided by
#	  AFNI under AFNI_HOME/bin/lib_realtime
# 
# RTInterface: the real-time socket interface, for receiving data
#              from the real-time plugin to afni over a TCP port.
#
# ----------------------------------------------------------------------

import lib_realtime as RT

#-----------------------------------------------------------------------------------------------------------
class AfniRt:

  def __init__(self, port, verbose):
    """ Initialise RTInterface object and define the TCP port and verbose level """
    
    # Afni RTInterface object
    self.RTI = RT.RTInterface()
    
    # Define the port
    self.RTI.server_port = port
    
    # Define verborse
    self.RTI.verb = verbose
    
    
  def open_incoming_socket(self):
    """Open the incoming socket number"""
    return self.RTI.open_incoming_socket()

  def wait_for_new_run(self):
    """Wait for new incoming data in socket"""
    return self.RTI.wait_for_new_run()
    
  def read_all_socket_data(self):
    """read incoming data"""
    return self.RTI.read_all_socket_data()
    
  def close_data_ports():
    """Closes the socket"""
    return self.RTI.close_data_ports()
        
  def get_rois_values(self):
    """ Returns a list of data with the ROI means value. The length will depend on the number of ROIs """
    return self.RTI.extras
    
  def get_rois_number(self):
    return self.RTI.nextra
    
#-----------------------------------------------------------------------------------------------------------
    
if __name__ == '__main__':
  print '** main is not supported in this library'