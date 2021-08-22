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

df_cust = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\Customers461.csv", usecols=["ID", "Name", "Phone", "Email", "Office Phone"], dtype=str)

df_cust.columns = df_cust.columns.str.lower()

df_cust.rename(columns={"office phone": "alt_phone", "name": "company"}, inplace=True)

# df_cust_original = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\Customers461.csv", usecols=["ID", "Name", "Company Name", "Phone", "Email", "Office Phone"])

###############################################################################################
df_cust["id"] = df_cust["id"].apply(lambda x: x[:-7].replace(" ", "") if "[" in x else x) #clean id
df_cust = df_cust.replace(np.nan, "", regex=True) #remove nan

def phone_cleaner(df, col):
    df[col] = df[col].apply(lambda x: x.replace(" ", ""))
    symbols = ["+", "-", "(", ")", ".", "_", "+", r"*", "/", "|", "\\"]
    for s in symbols:
        df[col] = df[col].apply(lambda x: x.replace(s, ""))
    df[col] = df[col].apply(lambda x: x.split(re.findall(r"[\D]", x)[0], 1)[0] if len(re.findall(r"[\D]", x)) > 0 else x)
    df[col] = df[col].apply(lambda x: x[-9:]) #last digits phone
    df.reset_index(drop=True, inplace=True)
        
phone_cleaner(df_cust, "phone")
phone_cleaner(df_cust, "alt_phone")

df_cust.drop(df_cust[(df_cust["phone"] == "") & (df_cust["email"] == "")].index, inplace=True) #drop w/o phone and email

alt_rows = df_cust.loc[df_cust["alt_phone"] != ""].reset_index(drop=True).drop(columns=["alt_phone"])
df_cust.drop(columns=["alt_phone"], inplace=True)
df_cust = pd.concat([df_cust, alt_rows], ignore_index=True).reindex(columns=["company", "phone", "email", "id"]) #cust df with alt phones
