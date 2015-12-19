#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from __future__ import division # use 3.x behaviour for division -- / for float, // for int.

print('test-utf:café') #.encode('utf-8') # test unicode script encoding.


import random
import csv
from sets import Set
import sys
import pprint #pretty print nested structures
from itertools import chain
from collections import Counter
import json

import numpy
import pymongo

from matplotlib.pyplot import *
from matplotlib.ticker import FixedLocator
import matplotlib
# https://github.com/matplotlib/matplotlib/blob/master/extern/ttconv/ex
# "RuntimeError: TrueType font file contains a very long PostScript name"
# https://github.com/matplotlib/matplotlib/issues/3206
#matplotlib.rcParams['font.family'] = 'serif'
#matplotlib.rcParams['font.serif'] = 'CMU Serif, Times New Roman'

#we want inline charts.
#get_ipython().magic(u'matplotlib inline')
sys.path.append('C:/work/code/3rd_Ben/matrix2latexPython/matrix2latex')
import matrix2latex

####################################################
############# data_dir needs a trailing slash! ################
####################################################
#data_dir = 'C:/work/data/output/PHD_DATA/2015-03-08/17.10.00_expset_bing_crosby_normal/Full/' ## LAST RUN -- NEW EDGE WEIGHTING
data_dir = "C:/work/data/output/PHD_DATA/2015-03-21/16.59.30_expset_bing_crosby_normal/Full/" # 
#data_dir ='C:/work/data/output/PHD_DATA/2015-03-02/14.37.53_expset_bing_crosby_normal/Full/' ## LAST RUN WITH OLD EDGE WEIGHTING


phd_output_dir = 'C:/work/docs/LATEX/thesis/images/'


total_gt_datums = 583 #using the mongo data from the laptop this seems to be the value.
#161 #this is then asserted against the calculated value.
