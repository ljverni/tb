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


df_main = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\Contacts484.csv")

# df_main_original = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\Contacts484.csv")

df_main.drop(df_main[df_main["Subsidiary"].str[-7:] == "Limited"].index, inplace=True) #Limited Subsidiary
df_main.drop(columns=["Duplicate", "Category", "Subsidiary", "Subsidiary.1", "Login Access", "Job Title", "Name"], inplace=True)
df_main.columns = df_main.columns.str.lower()
df_main.drop(df_main[(df_main["company"].isna()) | (df_main["company"].str[0] != "C")].index, inplace=True) #drop w/o company name and non customers
df_main.drop(df_main[(df_main["phone"].isna()) | (df_main["email"].isna())].index, inplace=True) #drop no contact info
df_main["id"] = df_main["company"] 
df_main["id"] = df_main["id"].apply(lambda x: x.split(" ")[0]) #id column
df_main["company"] = df_main["company"].apply(lambda x: " ".join(x.split(" ")[1:])) #remove id from company

def phone_cleaner():
    symbols = ["+", "-", "(", ")", ".", "_", "+", "*"]
    for s in symbols:
        df_main["phone"] = df_main["phone"].apply(lambda x: x.replace(s, ""))
    df_main["phone"] = df_main["phone"].apply(lambda x: x.split(re.findall(r"[a-zA-Z]", x)[0], 1)[0] if len(re.findall(r"[a-zA-Z]", x)) > 0 else x)
    df_main["phone"] = df_main["phone"].apply(lambda x: x.replace(" ", ""))
        
phone_cleaner()

df_main["company"] = df_main["company"].apply(lambda x: x.split("] ")[1] if len(x.split("] ")) > 1 else x) # remove company site

