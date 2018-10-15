import csv
import sys
import os
import shutil
import copy
try:
    import datetime
except:
    import pip
    pip.main(['install','datetime'])
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