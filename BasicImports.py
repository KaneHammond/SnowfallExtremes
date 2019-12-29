import csv
import sys
import os
import shutil
import copy
import subprocess
import math
import pylab as pl
import matplotlib.mlab as mlab
# try:
#     try:
#         import datetime
#     except:
#         subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'datetime', 'PyYAML==3.11'])
#         import datetime
#     try:
#         subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'datetime', 'PyYAML==3.11'])
#         import datetime
#     except:
#         pip install --ignore-installed six datetime
#         import datetime
# except:
#     print('Unable to install datetime through pip. Try sudo command')       
import datetime
from datetime import timedelta
from datetime import datetime

try:
    import matplotlib.pyplot as plt
except:
    import pip
    pip.main(['install','matplotlib.pyplot'])
    import matplotlib.pyplot as plt

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
# try:
#     import seaborn as sns
# except:
#     import pip
#     pip.main(['install','seaborn'])
#     import seaborn as sns
try:
    import scipy
except:
    import pip
    pip.main(['install','scipy'])
    import scipy 
from scipy import stats
from scipy.stats import norm
from scipy.stats import uniform
import collections

try:
    import tqdm
except:
    import pip
    pip.main(['install','tqdm'])
    import tqdm

import time

### ************************************
# ARIMA IMPORTS

# try:
#     import plotly
# except:
#     import pip
#     # from pip import _internal as pip
#     pip.main(['install','plotly'])
#     # subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'stats'])
# import plotly

# import plotly.plotly as ply

# try:
#     import cufflinks
# except:
#     import pip
#     # from pip import _internal as pip
#     pip.main(['install','cufflinks'])
#     # subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'stats'])
# import cufflinks

# import cufflinks as cf

# from plotly.plotly import plot_mpl
# from statsmodels.tsa.seasonal import seasonal_decompose