
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


from matplotlib.pyplot import  *
from matplotlib.ticker import FixedLocator


#we want inline charts.
#get_ipython().magic(u'matplotlib inline')
sys.path.append('C:/work/code/3rd_Ben/matrix2latexPython/matrix2latex')
import matrix2latex

import matplotlib
# https://github.com/matplotlib/matplotlib/blob/master/extern/ttconv/ex
# "RuntimeError: TrueType font file contains a very long PostScript name"
# https://github.com/matplotlib/matplotlib/issues/3206
#matplotlib.rcParams['font.family'] = 'serif'
#matplotlib.rcParams['font.serif'] = 'CMU Serif, Times New Roman'


####################################################
############# data_dir needs a trailing slash! ################
####################################################

#data_dir = 'C:/work/docs/Dropbox/PHD_DATA/'
#data_dir = 'C:/work/data/output/2014-11-21/17.42.12_expset/PhaseAOnlyExperimentSet/'
#data_dir = 'C:/work/docs/Dropbox/PHD_DATA/2014-11-29/17.33.55_expset_bing_crosby/Thesis_Experiment_Set/'
#data_dir = 'C:/work/data/output/2014-11-21/17.42.12_expset/PhaseAOnlyExperimentSet/'
data_dir = 'C:/work/docs/Dropbox/PHD_DATA/2015-02-01/19.36.38_expset_bing_crosby_normal/Full/'
data_dir_experimentset = 'C:/work/docs/Dropbox/PHD_DATA/2015-02-01/19.36.38_expset_bing_crosby_normal/'


phd_output_dir = 'C:/work/docs/PHD_work/thesis/images/'


total_gt_datums = 583 #using the mongo data from the laptop this seems to be the value.
#161 #this is then asserted against the calculated value.