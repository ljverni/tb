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


df_contacts = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\Contacts484.csv")

# df_contacts_original = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\Contacts484.csv")

df_contacts.drop(df_contacts[df_contacts["Subsidiary"].str[-7:] != "Limited"].index, inplace=True) #Limited Subsidiary
df_contacts.drop(columns=["Duplicate", "Category", "Subsidiary", "Subsidiary.1", "Login Access", "Job Title", "Name"], inplace=True)
df_contacts.columns = df_contacts.columns.str.lower()
df_contacts.drop(df_contacts[(df_contacts["company"].isna()) | (df_contacts["company"].str[0] != "C")].index, inplace=True) #drop w/o company name and non customers
df_contacts.drop(df_contacts[(df_contacts["phone"].isna()) | (df_contacts["email"].isna())].index, inplace=True) #drop no contact info
df_contacts["id"] = df_contacts["company"] 
df_contacts["id"] = df_contacts["id"].apply(lambda x: x.split(" ")[0]) #id column
df_contacts["company"] = df_contacts["company"].apply(lambda x: " ".join(x.split(" ")[1:])) #remove id from company

def phone_cleaner():
    df_contacts["phone"] = df_contacts["phone"].apply(lambda x: x.replace(" ", ""))
    symbols = ["+", "-", "(", ")", ".", "_", "+", r"*", "/", "|", "\\"]
    for s in symbols:
        df_contacts["phone"] = df_contacts["phone"].apply(lambda x: x.replace(s, ""))
    df_contacts["phone"] = df_contacts["phone"].apply(lambda x: x.split(re.findall(r"[\D]", x)[0], 1)[0] if len(re.findall(r"[\D]", x)) > 0 else x)
    df_contacts["phone"] = df_contacts["phone"].apply(lambda x: x[-9:]) #last digits phone
    df_contacts.reset_index(drop=True, inplace=True)
        
phone_cleaner()

df_contacts["company"] = df_contacts["company"].apply(lambda x: x.split("] ")[1] if len(x.split("] ")) > 1 else x) # remove company site






