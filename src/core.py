
import random
import csv
from sets import Set
import numpy


from collections import Counter
from matplotlib.pyplot import  *
from matplotlib.ticker import FixedLocator


#we want inline charts.
#get_ipython().magic(u'matplotlib inline')
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
data_dir = 'C:/work/docs/Dropbox/PHD_DATA/2015-02-01/19.36.38_expset_bing_crosby_normal/Full/'

#data_dir = 'C:/work/data/output/2014-11-21/17.42.12_expset/PhaseAOnlyExperimentSet/'