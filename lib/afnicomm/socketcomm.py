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
import datetime
import time

class TrValues:
    
    def __init__(self, rois, tr_number):
        self.rois = rois
        self.tr_number = tr_number

#-----------------------------------------------------------------------------------------------------------
class AfniRt:

  def __init__(self, options):
    """ Initialise RTInterface object and define the TCP port and verbose level """
    
    # Afni RTInterface object
    self.RTI = RT.RTInterface()
    
    # Define the port
    if options.port > 0:
      self.RTI.server_port =  options.port
    
    # Define verborse
    if options.debug > 0 and  options.debug < 4:
      self.RTI.verb = options.debug
      
    self.log = options.log
    
    if self.log:
        file_name = "run_%s.log" %time.time()
        self.file = open(file_name, "w+")
    
  def write_tr(self, tr, time, roi_values):
      text = str(tr) + '\t' + str(time) + '\t' + str(roi_values) + '\n'
      self.file.write(text)
    
  def open_incoming_socket(self):
    """Open the incoming socket number"""
    result = self.RTI.open_incoming_socket()
    
    if not result:
        if self.log and not self.file.closed:
            self.file.write('## Socket openned\n')
        
    return result

  def wait_for_new_run(self):
    """Wait for new incoming data in socket"""
    result = self.RTI.wait_for_new_run()
    
    if not result:
        if self.log and not self.file.closed:
            self.file.write('\n## New Run\n')
        
    return result
    
  def read_TR_data(self):
    """read incoming data"""
    result = self.RTI.read_TR_data()
    
    if not result:
        if self.log and not self.file.closed:
            self.write_tr(self.RTI.nread, 
                          datetime.datetime.now().strftime("%H:%M:%S.%f"), 
                          self.get_last_roi_values(self.get_rois_values()))
        
    return result
    
  def close_data_ports(self):
    """Closes the socket"""
    result = self.RTI.close_data_ports()

    if self.log and not self.file.closed:
        self.file.write('\n## Closing...\n')
        self.file.close()
    
    return result
	
  def get_rois_values(self):
    """ Returns a list of data with the ROI means value. The length will depend on the number of ROIs """
    return self.RTI.extras
    
  def get_rois_number(self):
    """ Return the number of ROIs received """
    return self.RTI.nextra

  def get_num_read(self):
    """ Returns the number of TR read per connection"""
    return self.RTI.nread
    
  
  def get_last_roi_values(self, rois_values):
    """                                 ROI1            ROI2                 ROIN
    values is a matrix with format [[TR,TR,TR,...], [TR,TR,TR,...],... , [TR,TR,TR,...]]    
    """
    last_values = []
    for roi in rois_values:
        if len(roi) > 0:
            last_values.append(roi[-1])
        
    return last_values
    
  def get_last_values(self):
    """
    Returns the last roi values together with the TR sequence number
    """

    if len(self.get_rois_values()) > 0:           
        roi_values = TrValues(self.get_last_roi_values(self.get_rois_values()), 
                              self.get_num_read())
    else:
        roi_values = TrValues([],0)
      
    yield roi_values
    
    
#-----------------------------------------------------------------------------------------------------------
    
if __name__ == '__main__':
  print('** main is not supported in this library')
