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
from ns_customers import df_cust

df_con = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\Contacts484.csv")

# df_con_original = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\Contacts484.csv")

df_con.drop(df_con[df_con["Subsidiary"].str[-7:] != "Limited"].index, inplace=True) #Limited Subsidiary
df_con.drop(columns=["Duplicate", "Category", "Subsidiary", "Subsidiary.1", "Login Access", "Job Title", "Name"], inplace=True)
df_con.columns = df_con.columns.str.lower()
df_con.drop(df_con[df_con["company"].isna()].index, inplace=True) #drop w/o company name
df_con.drop(df_con[(df_con["phone"].isna()) | (df_con["email"].isna())].index, inplace=True) #drop no contact info
df_con["id"] = df_con["company"] 
df_con["id"] = df_con["id"].apply(lambda x: x.split(" ")[0]) #id column
df_con["company"] = df_con["company"].apply(lambda x: " ".join(x.split(" ")[1:])) #remove id from company

def phone_cleaner(df, col):
    df[col] = df[col].apply(lambda x: x.replace(" ", ""))
    symbols = ["+", "-", "(", ")", ".", "_", "+", r"*", "/", "|", "\\"]
    for s in symbols:
        df[col] = df[col].apply(lambda x: x.replace(s, ""))
    df[col] = df[col].apply(lambda x: x.split(re.findall(r"[\D]", x)[0], 1)[0] if len(re.findall(r"[\D]", x)) > 0 else x)
    df[col] = df[col].apply(lambda x: x[-9:]) #last digits phone
    df.reset_index(drop=True, inplace=True)
        
phone_cleaner(df_con, "phone")

df_con["company"] = df_con["company"].apply(lambda x: x.split("] ")[1] if len(x.split("] ")) > 1 else x) # remove company site

df_con = pd.concat([df_con, df_cust], ignore_index=True)




