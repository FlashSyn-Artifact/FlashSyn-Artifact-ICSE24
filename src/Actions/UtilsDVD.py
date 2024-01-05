import os
import sys
import inspect

from black import Line

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir) 
print(parentdir)

from src.forge.forgeCollect import *
import itertools
import time
import scipy.optimize as optimize
import builtins

from scipy.interpolate import griddata, interp1d
import scipy.optimize as optimize
from scipy.interpolate import NearestNDInterpolator
from scipy.interpolate import LinearNDInterpolator


from scipy.spatial.qhull import QhullError

import signal
import numpy as np



def buildDVDattackContract(ActionList):
    allActionStr = ""
    for i in range(len(ActionList)):
        temp = ActionList[i].actionStr()
        allActionStr += temp
    
    return allActionStr

def buildDVDCollectorContract(ActionList):
    allCollectorStr = ""
    for i in range(len(ActionList) - 1):
        temp = ActionList[i].actionStr()
        allCollectorStr += temp
    allCollectorStr += ActionList[-1].collectorStr()
    return allCollectorStr



