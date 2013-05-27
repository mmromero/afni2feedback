#!/usr/bin/env python

# ----------------------------------------------------------------------
# This module contains the unit test for afnicomm/socketcomm.py
# ----------------------------------------------------------------------
import sys
sys.path.append('../lib')
import unittest
from mock import MagicMock
from afnicomm import socketcomm as SC

#---- Constants ------

NEGATIVE_PORT = -10000
POSSITIVE_PORT = 10000
DEFAULT_PORT = 53214

NEGATIVE_DEBUG = -1
POSSITIVE_DEBUG = 3
DEFAULT_DEBUG = 1

ERROR   = 1
SUCCESS = 0

#---------------------


class TestSocketComm(unittest.TestCase):
  
  def test__init__port_negative(self):
    """ Must use default port """
    ar = SC.AfniRt(NEGATIVE_PORT, POSSITIVE_DEBUG)
    self.assertEquals(DEFAULT_PORT,ar.RTI.server_port)
    
  def test__init__debug_negative(self):
    """ Must use default level"""
    ar = SC.AfniRt(POSSITIVE_PORT, NEGATIVE_DEBUG)
    self.assertEquals(DEFAULT_DEBUG,ar.RTI.verb)
    
  def test__init__(self):
    """ When everything is right must return SUCCESS code """
    ar = SC.AfniRt(POSSITIVE_PORT, POSSITIVE_DEBUG)
    self.assertEquals(POSSITIVE_DEBUG,ar.RTI.verb)
    self.assertEquals(POSSITIVE_PORT,ar.RTI.server_port)
  
  def test_open_incoming_socket_fail(self):
    """ When an error occurs opening the socket must return ERROR
    code"""
    ar = SC.AfniRt(POSSITIVE_PORT, DEFAULT_DEBUG)
    ar.RTI.open_incoming_socket = MagicMock(return_value=ERROR)
    self.assertEquals(ERROR,ar.open_incoming_socket())
     
  def test_open_incoming_socket_success(self):
    """ When socket is opened successfully must return SUCCESS code"""
    ar = SC.AfniRt(POSSITIVE_PORT, DEFAULT_DEBUG)
    ar.RTI.open_incoming_socket = MagicMock(return_value=SUCCESS)
    self.assertEquals(SUCCESS,ar.open_incoming_socket())

  def test_wait_for_new_run_error(self):
    """ When an error occurs waiting for new run must return ERROR
    code"""
    ar = SC.AfniRt(POSSITIVE_PORT, DEFAULT_DEBUG)
    ar.RTI.wait_for_new_run = MagicMock(return_value=ERROR)
    self.assertEquals(ERROR,ar.wait_for_new_run())
     
  def test_wait_for_new_run_success(self):
    """ When new run arrives successfully must return SUCCESS code"""
    ar = SC.AfniRt(POSSITIVE_PORT, DEFAULT_DEBUG)
    ar.RTI.wait_for_new_run = MagicMock(return_value=SUCCESS)
    self.assertEquals(SUCCESS,ar.wait_for_new_run())  
  
  def test_read_all_socket_data_error(self):
    """ When an error occurs while reading new data, this must return ERROR code"""
    ar = SC.AfniRt(POSSITIVE_PORT, DEFAULT_DEBUG)
    ar.RTI.read_all_socket_data = MagicMock(return_value=ERROR)
    self.assertEquals(ERROR,ar.read_all_socket_data())
     
  def test_read_all_socket_data_success(self):
    """ When new data is read successfully must return SUCCESS code"""
    ar = SC.AfniRt(POSSITIVE_PORT, DEFAULT_DEBUG)
    ar.RTI.read_all_socket_data = MagicMock(return_value=SUCCESS)
    self.assertEquals(SUCCESS,ar.read_all_socket_data())  
    
  def test_close_data_ports(self):
    """ Check that calling close_data_ports RTI.close_data_ports is called"""
    ar = SC.AfniRt(POSSITIVE_PORT, DEFAULT_DEBUG)
    ar.RTI.close_data_ports = MagicMock(return_value=None)
    
    # Call the method
    ar.close_data_ports()
    
    # Check it was called
    ar.RTI.close_data_ports.assert_called_with()
    
  def test_get_rois_values_no_rois(self):
    """ When there are no ROIs, empty list is returned """
    ar = SC.AfniRt(POSSITIVE_PORT, DEFAULT_DEBUG)
    #Prepare the mock
    ar.RTI.extras = []
    
    #Assert
    self.assertEquals([],ar.get_rois_values())
   
  def test_get_rois_values_2_rois(self):
    """ When there are mutliple ROIs, a list with length the number of rois must be returned """
    ar = SC.AfniRt(POSSITIVE_PORT, DEFAULT_DEBUG)
    #Prepare the mock
    ar.RTI.extras = [1, 2]
    
    #Assert
    self.assertEquals([1, 2],ar.get_rois_values())
    
  def test_get_rois_number_no_rois(self):
    """ When no ROIS 0 must be returned """
    ar = SC.AfniRt(POSSITIVE_PORT, DEFAULT_DEBUG)
    #Prepare the mock
    ar.RTI.nextra = 0
    
    #Assert
    self.assertEquals(0,ar.get_rois_number())
    
  def test_get_rois_number_multiple_rois(self):
    """ When no ROIS 0 must be returned """
    ar = SC.AfniRt(POSSITIVE_PORT, DEFAULT_DEBUG)
    #Prepare the mock
    ar.RTI.nextra = 3
    
    #Assert
    self.assertEquals(3,ar.get_rois_number())
      
# ----------------------------------------------------------------------
if __name__ == '__main__':
  unittest.main()