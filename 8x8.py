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



df_main = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\Call_Records_2021-01-01-2021-06-30.csv")

# df_main_original = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\Call_Records_2021-01-01-2021-06-30.csv")

agent_dic = {"Ali Al-Fadhli": "10516", "Alex Seater": "10302", "Callum Lawrence": "10300", "Ellie Puddephatt": "10496", "Joseph Keane": "10370", "Karl Fisher": "10489", "Luciano Verni": "10515", "Madeleine Johnson": "10459", "Tom Skinner": "10365", "Vince Canard": "10735"}

df_main = df_main.drop(columns=["Call ID", "Start Time", "Call Time", "Ring Duration", "Missed", "Abandoned"])
df_main.columns = df_main.columns.str.lower().str.replace(" ", "_")
df_main.drop(df_main[df_main.answered != "Answered"].index, inplace=True) #drop unanswered rows
df_main.drop(df_main[df_main.answered != "Answered"].index, inplace=True) #drop unanswered rows
df_main.drop(columns=["answered"], inplace=True)
df_main["date"] = df_main["answered_time"].apply(lambda x: str(x)[3:6] + str(x)[0:3] + str(x)[6:10]) #date col
df_main["answered_time"] = df_main["answered_time"].apply(lambda x: str(x)[11:])
df_main["stop_time"] = df_main["stop_time"].apply(lambda x: str(x)[11:])
df_main["caller"] = df_main["caller"].apply(lambda x: x.replace("+44", "") if x[:3] == "+44" else x) #removing +44
df_main["callee"] = df_main["callee"].apply(lambda x: x.replace("+44", "") if x[:3] == "+44" else x) #removing +44
df_main["caller"] = df_main["caller"].apply(lambda x: x.replace("+", "") if x[0] == "+" else x) #removing +
df_main["callee"] = df_main["callee"].apply(lambda x: x.replace("+", "") if x[0] == "+" else x) #removing +
df_main["caller"] = df_main["caller"].apply(lambda x: "click" if "ClickToDial" in x else x) #clicktodial
df_main.loc[df_main["caller"] == "click", "caller"] = df_main.loc[df_main["caller"] == "click", "caller_name"] #clicktodial replaced
df_main.loc[(df_main["direction"] == "Incoming")&(df_main["caller_name"].notnull()), "direction"] = "Internal" #incoming internal
df_main.drop(df_main[(df_main["callee"] == "bargeService") | (df_main["callee"] == "Voicemail") | (df_main["callee"] == "RingGroup") | (df_main["callee"] == "CallRecording")].index, inplace=True) #drop callee bargeService, Voicemail, Ringroup, CallRecording
df_main.drop(df_main[((df_main["callee"].isnull()) & (df_main["callee_name"].isnull())) | ((df_main["caller"].isnull()) & (df_main["caller_name"].isnull()))].index, inplace=True) #drop no caller&caller name
df_main.loc[df_main["caller_name"].notnull(), "caller"] = df_main.loc[df_main["caller_name"].notnull(), "caller_name"] #replace caller with caller name
df_main.loc[df_main["callee_name"].notnull(), "callee"] = df_main.loc[df_main["callee_name"].notnull(), "callee_name"] #replace callee with callee name
df_main.drop(columns=["caller_name", "callee_name"], inplace=True) #drop callee_name & caller_name
df_main = df_main[(df_main["caller"].isin(agent_dic.keys())) | (df_main["callee"].isin(agent_dic.keys()))].reset_index(drop=True) #drop calls without agents
# df_main.loc[df_main["caller"] ]

test = df_main[(df_main["date"]=="16/06/2021")&(df_main["callee"]=="Vince Canard")]