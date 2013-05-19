import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
sys.path.append('/usr/lib/afni/bin/')
import lib_realtime as RT

RTI = RT.RTInterface();

if RTI:
  print RTI
else:
  print "No realtime lib"