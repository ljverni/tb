import pandas as pd
from datetime import datetime
import calendar
import numpy as np
from datetime import timedelta
import json
import re
from matplotlib.gridspec import GridSpec
from matplotlib.legend import Legend
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.lines import Line2D
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib import pyplot as plt
plt.style.use("seaborn")
from numpy import inf

from eight import *
from ns_contacts import *


def add_customer_name():
    df_ext["customer"] = ""
    for index, row in df_con.iterrows():
        df_ext.loc[df_ext["customer_phone"] == row["phone"], "customer"] = row["company"]
add_customer_name()


test = df_ext.loc[df_ext["customer"] == ""]