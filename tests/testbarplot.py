#!/usr/bin/env python

# ----------------------------------------------------------------------
# This module contains the unit test for gui/barplot.py
# ----------------------------------------------------------------------
import sys
sys.path.append('../lib')
import unittest
from mock import patch
from mock import MagicMock
from gui import barplot as BP
import matplotlib.pyplot

#---- Constants ------

DEFAULT_IS_TRHOLD = 0
DEFAULT_THRESHOLD = 0
DEFAULT_DEBUG = 1

THRESHOLD_DEF = 1

ERROR   = 1
SUCCESS = 0

#---------------------
class TestBarplot(unittest.TestCase):

  def setUp(self):
    self.patcher = patch('matplotlib.pyplot', spec=True)
    MockClass = self.patcher.start()
    self.plt = MockClass()

  def tearDown(self):
    self.patcher.stop()
  
  def test__init__barplot(self):
    """ Must use default port """
    self.plt.ion = MagicMock(return_value=SUCCESS)
    self.plt.show = MagicMock(return_value=SUCCESS)
    
    bp = BP.BarPlotter(self.plt, DEFAULT_DEBUG)
    
    self.assertEquals(DEFAULT_THRESHOLD,bp.threshold)
    self.assertEquals(DEFAULT_DEBUG,bp.verbose)
    self.assertEquals(DEFAULT_IS_TRHOLD, bp.isThresholdDef)
    
    self.plt.ion.assert_called_with()
    self.plt.show.assert_called_with()
    
  def test_set_threshold(self):
    """ Test set_threshold method """
    bp = BP.BarPlotter(self.plt, DEFAULT_DEBUG)
    
    bp.set_threshold(200)
    
    self.assertEquals(THRESHOLD_DEF, bp.isThresholdDef)
    self.assertEquals(200, bp.threshold)
    self.plt.axhline.asser_called_with(y=200)
    
  def test_draw_new_values_empty_values(self):
    """ Test draw method when no values are provided """
 
    bp = BP.BarPlotter(self.plt, DEFAULT_DEBUG)
    
    bp.draw_new_values(())
    self.assertFalse(self.plt.bar.called)
    
  def test_draw_new_values_many_values(self):
    bp = BP.BarPlotter(self.plt, DEFAULT_DEBUG)
    
    bp.draw_new_values((1, 2))
    self.assertTrue(self.plt.bar.called)
    
    
# -----------------------------------------------------------
if __name__ == '__main__':
  unittest.main()
