import sys
sys.path.append('../lib')
import unittest
from mock import MagicMock
from mock import patch
from main import Neurofeedback
from afnicomm import socketcomm 
import matplotlib.pyplot

ERROR   = 1
SUCCESS = 0

#-------------------------------------------------- 

class TestSocketComm(unittest.TestCase):

  def setUp(self):
    self.pltPatcher = patch('matplotlib.pyplot', spec=True)
    self.comPatcher = patch('afnicomm.socketcomm', spec=True)
    MockPlt = self.pltPatcher.start()
    MockCom = self.comPatcher.start()
    self.plt = MockPlt()
    self.com = MockCom()

  def tearDown(self):
    self.pltPatcher.stop()
    self.comPatcher.stop()

  def test_error_opening_incoming_socket(self):
    self.com.open_incoming_socket = MagicMock(return_value=ERROR)

    nfb = Neurofeedback(self.com, self.plt)

    nfb.run()

    self.com.open_incoming_socket.assert_called_with()
    self.com.close_data_ports.assert_called_with()

  def test_error_waiting_for_new_run(self):
    self.com.open_incoming_socket = MagicMock(return_value=SUCCESS)
    self.com.wait_for_new_run = MagicMock(return_value=ERROR)

    nfb = Neurofeedback(self.com, self.plt)

    nfb.run()

    self.com.wait_for_new_run.assert_called_with()
    self.com.close_data_ports.assert_called_with()    

  def test_error_reading_all_socket_data(self):
    self.com.open_incoming_socket = MagicMock(return_value=SUCCESS)
    self.com.wait_for_new_run = MagicMock(return_value=SUCCESS)
    self.com.read_all_socket_data = MagicMock(return_value=ERROR)

    nfb = Neurofeedback(self.com, self.plt)

    nfb.run()

    self.com.read_all_socket_data.assert_called_with()
    self.com.close_data_ports.assert_called_with()

  
    
#-------------------------------------------------- 
if __name__ == '__main__':
  unittest.main()
