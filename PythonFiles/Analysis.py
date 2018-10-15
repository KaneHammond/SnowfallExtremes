
print "Analysis Imported"
import csv
import sys
import os
import shutil
import copy
try:
    import scipy
except:
    import pip
    pip.main(['install','scipy'])
    import scipy
try:
    import datetime
except:
    import pip
    pip.main(['install','datetime'])
    import datetime
#*****NOTE: CHECK matplotlib vs matplotlib.pyplot. Failed to import without the latter.
#*****NOTE: CHECK matplotlib vs matplotlib.pyplot. Failed to import without the latter.
#*****NOTE: CHECK matplotlib vs matplotlib.pyplot. Failed to import without the latter.
try:
    import matplotlib as plt
except:
    import pip
    pip.main(['install','matplotlib'])
    import matplotlib as plt
try:
    import matplotlib.pyplot as plt
except:
    import pip
    pip.main(['install','matplotlib.pyplot'])
    import matplotlib.pyplot as plt
#*****NOTE: CHECK matplotlib vs matplotlib.pyplot. Failed to import without the latter.
#*****NOTE: CHECK matplotlib vs matplotlib.pyplot. Failed to import without the latter.
#*****NOTE: CHECK matplotlib vs matplotlib.pyplot. Failed to import without the latter.
try:
    import numpy as np
except:
    import pip
    pip.main(['install','numpy'])
    import numpy as np
try:
    import pandas as pd
except:
    import pip
    pip.main(['install','pandas'])
    import pandas as pd
try:
    import seaborn as sns
except:
    import pip
    pip.main(['install','seaborn'])
    import seaborn as sns
try:
    import scipy
except:
    import pip
    pip.main(['install','scipy'])
    import scipy 
import scipy.stats
from scipy.stats import norm
from scipy.stats import uniform
import collections
from scipy import stats
import copy
from copy import deepcopy
from decimal import Decimal
from datetime import datetime
import matplotlib.pyplot as plt; plt.rcdefaults()
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import NullFormatter
import time
from Snowfall import *
sys.path.append("PythonFiles")

### CDF Thresholds
# Snowfall Extremes
SE = (Decimal('0.95').normalize())

### GRAPHICAL OUTPUT SELECTION

f = 'pdf' # Defines graphical output format

### First year in downloaded data set/target start year.
FirstYear = 1950

print Data
### PROCESS RAW DATA
import SplitData
SplitData
from SplitData import *

# ### SNOWFALL ANALYSIS
# import Snowfall_Analysis
# Snowfall_Analysis
# from Snowfall_Analysis import *

# # ## TEMP ANALYSIS
# import Temperature_Analysis
# Temperature_Analysis
# from Temperature_Analysis import *
#*#*#*#*#*#*#*#*#*#*# FORMAT #*#*#*#*#*#*#*#*#*#*#*#*#
#*#*# [Station, EE Slope, EE p, #SD Slope, #SD p, AS Slope, AS p, StD Slope, StD p]

# print (FinalData)

# FinalData[0] = FinalData[0].replace(",", "--")
# FinalDataStr = str(FinalData)
# FinalDataStr = FinalDataStr.replace("[", "")
# FinalDataStr = FinalDataStr.replace("]", "")

# Edit = open('TotalOutSO.csv', 'a')
# #for aLine in FinalData:
# Edit.write(FinalDataStr)
# Edit.write("\n")
# Edit.write(FinalData)