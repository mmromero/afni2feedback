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

from . import lib_realtime as RT

class TrValues:
    
    def __init__(self, rois, tr_number):
        self.rois = rois
        self.tr_number = tr_number

#-----------------------------------------------------------------------------------------------------------
class AfniRt:

  def __init__(self, port, verbose):
    """ Initialise RTInterface object and define the TCP port and verbose level """
    
    # Afni RTInterface object
    self.RTI = RT.RTInterface()
    
    # Define the port
    if port > 0:
      self.RTI.server_port = port
    
    # Define verborse
    if verbose > 0 and verbose < 4:
      self.RTI.verb = verbose
    
    
  def open_incoming_socket(self):
    """Open the incoming socket number"""
    return self.RTI.open_incoming_socket()

  def wait_for_new_run(self):
    """Wait for new incoming data in socket"""
    return self.RTI.wait_for_new_run()
    
  def read_TR_data(self):
    """read incoming data"""
    return self.RTI.read_TR_data()
    
  def close_data_ports(self):
    """Closes the socket"""
    self.RTI.close_data_ports()
    return
	
  def get_rois_values(self):
    """ Returns a list of data with the ROI means value. The length will depend on the number of ROIs """
    return self.RTI.extras
    
  def get_rois_number(self):
    """ Return the number of ROIs received """
    return self.RTI.nextra

  def get_num_read(self):
    """ Returns the number of TR read per connection"""
    return self.RTI.nread
    
  def get_last_values(self):
    """                                 ROI1            ROI2                 ROIN
    values is a matrix with format [[TR,TR,TR,...], [TR,TR,TR,...],... , [TR,TR,TR,...]]    
    """
    if len(self.get_rois_values()) > 0:
        last_values = []
        rois_values = self.get_rois_values()
        for roi in rois_values:
            if len(roi) > 0:
                last_values.append(roi[-1])
            
        roi_values = TrValues(last_values, self.get_num_read())
    else:
        roi_values = TrValues([],0)
      
    yield roi_values
    
    
#-----------------------------------------------------------------------------------------------------------
    
if __name__ == '__main__':
  print('** main is not supported in this library')
