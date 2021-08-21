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

#MAIN DATAFRAME###############################################################

df_main = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\Call_Records_2021-01-01-2021-06-30.csv")

# df_main_original = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\Call_Records_2021-01-01-2021-06-30.csv")

agent_dic = {"Ali Al-Fadhli": "10516", "Alex Seater": "10302", "Callum Lawrence": "10300", "Ellie Puddephatt": "10496", "Joseph Keane": "10370", "Karl Fisher": "10489", "Luciano Verni": "10515", "Madeleine Johnson": "10459", "Tom Skinner": "10365", "Vince Canard": "10735"}


df_main = df_main.drop(columns=["Call ID", "Start Time", "Call Time", "Ring Duration", "Missed", "Abandoned"])
df_main.columns = df_main.columns.str.lower().str.replace(" ", "_")

def clean_agents(x):
    x = str(x)
    if len(x) == 7 and x[0] == "+":
        return x[2:]
    elif len(x) == 6 and x[0] == "+":
        return x[1:]
    elif len(x) == 6 and x[0] == "1":
        return x[1:]
    else:
        return x
    
def empty_agents():
    for key in agent_dic.keys():
        df_main.loc[df_main["callee_name"] == key, "callee"] = agent_dic[key]
        df_main.loc[df_main["caller_name"] == key, "caller"] = agent_dic[key]

df_main["callee"] = df_main["callee"].apply(clean_agents)
df_main["caller"] = df_main["caller"].apply(clean_agents)
empty_agents()



df_main = df_main[(df_main["caller"].isin(agent_dic.values())) | (df_main["callee"].isin(agent_dic.values()))].reset_index(drop=True) #drop calls without agents



df_main.drop(df_main[df_main.answered != "Answered"].index, inplace=True) #drop unanswered rows

df_main.drop(columns=["answered"], inplace=True)
df_main["date"] = df_main["answered_time"].apply(lambda x: str(x)[3:6] + str(x)[0:3] + str(x)[6:10]) #date col
df_main["answered_time"] = df_main["answered_time"].apply(lambda x: str(x)[11:])
df_main["stop_time"] = df_main["stop_time"].apply(lambda x: str(x)[11:])
df_main["caller"] = df_main["caller"].apply(lambda x: x.replace("+44", "") if x[:3] == "+44" else x) #removing +44
df_main["callee"] = df_main["callee"].apply(lambda x: x.replace("+44", "") if x[:3] == "+44" else x) #removing +44
df_main["caller"] = df_main["caller"].apply(lambda x: x.replace("+", "") if x[0] == "+" else x) #removing +
df_main["callee"] = df_main["callee"].apply(lambda x: x.replace("+", "") if x[0] == "+" else x) #removing +
df_main["caller"] = df_main["caller"].apply(lambda x: x[1:] if x not in agent_dic.keys() and len(x) > 5 else x) #remove first number of external phone


df_main.drop(df_main[(df_main["caller"].str[4:10] == "ToDial") | (df_main["caller"] == "nonymous")].index, inplace=True) #drop clicktodial & anonymous
df_main.drop(df_main[(df_main["callee"] == "bargeService") | (df_main["callee"] == "Voicemail") | (df_main["callee"] == "RingGroup") | (df_main["callee"] == "CallRecording")].index, inplace=True) #drop callee bargeService, Voicemail, Ringroup, CallRecording
df_main.drop(df_main[((df_main["callee"].isnull()) & (df_main["callee_name"].isnull())) | ((df_main["caller"].isnull()) & (df_main["caller_name"].isnull()))].index, inplace=True) #drop no calle&caller

def name_for_id(df):
    for key in agent_dic:
        df.replace(agent_dic[key], key, inplace=True)
    return df

name_for_id(df_main)


df_main.drop(columns=["caller_name", "callee_name"], inplace=True) #drop callee_name & caller_name
df_main = df_main[(df_main["caller"].isin(agent_dic.keys())) | (df_main["callee"].isin(agent_dic.keys()))].reset_index(drop=True) #drop calls without agents
df_main["answered_time"] = df_main["answered_time"].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())
df_main["stop_time"] = df_main["stop_time"].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time()) #datetime stop
df_main["talk_time"] = df_main["talk_time"].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time()) #datetime talk
df_main["date"] = df_main["date"].apply(lambda x: datetime.strptime(x, "%d/%m/%Y").date()) #datetime date

df_main.loc[df_main["caller"].str.len() == 5, "direction"] = "Internal" #set internal caller
df_main.loc[df_main["callee"].str.len() == 5, "direction"] = "Internal" #set internal callee
df_main.loc[((df_main["callee"].isin(agent_dic.keys())) & (df_main["caller"].isin(agent_dic.keys()))), "direction"] = "Internal" #set internal agents

condition1 = ((df_main["callee"].isin(agent_dic.keys())) & (df_main["caller"].isin(agent_dic.keys())))
condition2 = (((df_main["callee"].str.len() <= 5)) | (df_main["caller"].str.len() <= 5))
df_ext = df_main.drop(df_main[condition1 | condition2].index) #EXTERNAL DF
df_int = df_main[condition1 | condition2] #INTERNAL DF

#EXTERNAL DATAFRAME###########################################################
df_ext["agent"] = ""
df_ext.loc[df_ext["caller"].isin(agent_dic.keys()), "agent"] = df_ext.loc[df_ext["caller"].isin(agent_dic.keys())]["caller"] #send TB caller to agent col
df_ext.loc[df_ext["callee"].isin(agent_dic.keys()), "agent"] = df_ext.loc[df_ext["callee"].isin(agent_dic.keys())]["callee"] #send TB callee to agent col
df_ext.loc[df_ext["callee"].isin(agent_dic.keys()), "callee"] = df_ext.loc[df_ext["callee"].isin(agent_dic.keys())]["caller"] #send callee to caller col
df_ext.drop(columns=["caller"], inplace=True)
df_ext.rename(columns={"callee": "customer"}, inplace=True)
df_ext.reset_index(drop=True, inplace=True)

######################################################################################

