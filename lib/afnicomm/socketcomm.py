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
    
    # Store the number of volumes per resting and activation period
    self.number_volues = options.numvols
    
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
        self.file.write('## Executing wiht parameters: \n')
        self.file.write('## \tPlot: ' + str(options.plot) + ' \n')
        self.file.write('## \tDebug: ' + str(options.debug) + '\n')
        if options.threshold:
            self.file.write('## \tThreshold: ' + str(options.threshold) + ' %\n')
        self.file.write('## \tRecord: ' + str(options.record) + '\n')
        self.file.write('## \tNumber of volumes for resting: ' + str(options.numvols) + ' \n')
        self.file.write('## \tPort: ' + str(options.port) + '\n')
        self.file.write('\n')
    
  def write_log(self, text):
      if self.log:
        self.file.write(str(text))

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
            # If the module is zero it is the first value in resting or activation
            if self.get_num_read() % self.number_volues == 0:
                # If is resting
                if self.is_resting_period():
                    self.file.write('\n## Resting number ' + str((self.get_num_read() - self.number_volues )/ (self.number_volues*2)) + '\n')
                else:
                    self.file.write('\n## Activation number ' + str((self.get_num_read() - self.number_volues) / (self.number_volues*2)) + '\n')

            self.write_tr(self.get_num_read(), 
                          datetime.datetime.now().strftime("%H:%M:%S.%f"), 
                          self.get_last_roi_values(self.get_rois_values()))
        
    return result
    
  def is_closed(self):
      return self.RTI.socket_has_closed()
    
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
    """ Returns the number of TR read per connection, zero based"""
    return self.RTI.nread - 1
  
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
    


  def is_resting_period(self):
      """
      Resting periods are always at the begining of the cycle:
          
       |           |              |
       |           |              |
       | RESTING 0 | ACTIVATION 0 | ...
       |           |              |
       |           |              |
      """
      result = False

      if self.get_num_read() < self.number_volues:
         result = True
         
      else:
          # Shift the TRs number for an easy block detection
          nread = self.get_num_read() - self.number_volues 

          # If the division result is even it is resting, otherwise activation
          if (nread / self.number_volues) % 2 == 0 :
            result = True
    
      return result
      
    
#-----------------------------------------------------------------------------------------------------------
    
if __name__ == '__main__':
  print('** main is not supported in this library')
