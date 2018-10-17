import csv
import sys
import os
import shutil
import copy
import subprocess
# try:
#     import datetime
# except:
#     import pip
#     pip.main(['install','datetime'])
#     import datetime

# Test this method
try:
    try:
        import datetime
    except:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'datetime', 'PyYAML==3.11'])
        import datetime
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'datetime', 'PyYAML==3.11'])
        import datetime
    except:
        pip install --ignore-installed six datetime
        import datetime
except:
    print('Unable to install datetime through pip. Try sudo command')       

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
from scipy import stats
from scipy.stats import norm
from scipy.stats import uniform
import collections
import tqdm
import time