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
from time import perf_counter

df_opp = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\CustomOpportunityDashboardViewResults926.csv")

# df_opp_original = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\CustomOpportunityDashboardViewResults926.csv")

rep_dict = {"Eleanor Puddephatt": "E1034", "Vincent Canard": "E1049", "Joseph Keane": "E1357", "Callum Lawrence": "E1364", "Thomas Skinner": "E1382", "Karl Fisher": "E1403", "Madeleine Johnson": "E1415", "Ali Al-Fadhli": "E1434", "Luciano Verni": "E1442", "David Jones": "E1576"}

df_opp.columns = df_opp.columns.str.lower().str.replace(" ", "_")
df_opp.rename(columns={"projected_total": "gp", "sales_rep": "sales_rep_2", "opportunity_status": "status"}, inplace=True)

def clean_gp():
    for symbol in [",", "(", ")"]: #remove symbols from amount
        df_opp["gp"] = df_opp["gp"].apply(lambda x: (x.replace(symbol, ""))) 
    df_opp["gp"] = df_opp["gp"].astype(float)
clean_gp()

df_opp["date"] = df_opp["date"].apply(lambda x: datetime.strptime(x, "%d/%m/%Y")) #drop 2021
df_opp.drop(df_opp.loc[df_opp["date"].dt.year == 2020].index, inplace=True)
df_opp["date"] = df_opp["date"].apply(lambda x: x.date())

df_opp.loc[df_opp["sales_rep_2"].isna(), "sales_rep_2"] = df_opp.loc[df_opp["sales_rep_2"].isna(), "sales_rep_1"] #remove nan from rep
df_opp.loc[df_opp["sales_rep_1"].isna(), "sales_rep_1"] = df_opp.loc[df_opp["sales_rep_1"].isna(), "sales_rep_2"] #remove nan from rep1

df_opp["sales_rep_2"] = df_opp["sales_rep_2"].apply(lambda x: x.split(" ", 1)[1]) #removing id from rep
df_opp["sales_rep_1"] = df_opp["sales_rep_1"].apply(lambda x: x.split(" ", 1)[1]) #removing id from rep1

df_opp["title"].replace(np.nan, "No title", inplace=True) #replace nan titles

df_opp.drop(df_opp.loc[~df_opp["sales_rep_1"].isin(rep_dict.keys())].index, inplace=True) #drop non end user team



#ANALYTICS
open_byrep = df_opp.loc[(df_opp["status"] != "Closed Won") & (df_opp["status"] != "Closed Lost")].groupby(by=["sales_rep_1", "status"], as_index=False).agg({"date": "count", "gp": "sum"}).rename(columns={"date": "count"})

won_byrep = df_opp.loc[(df_opp["status"] == "Closed Won") | (df_opp["status"] == "Closed Lost")].groupby(by=["sales_rep_1", "status"], as_index=False).agg({"date": "count", "gp": "sum"}).rename(columns={"date": "count"})

opp_bydate = df_opp.groupby(by=["date", "sales_rep_1"], as_index=False).agg({"gp": "count"}).rename(columns={"gp": "opportunity"})


df = opp_bydate.loc[opp_bydate["sales_rep_1"] == "Luciano Verni"].sort_values(by="date", ascending=True)

def graphing(exec):
    date_range = [df_opp.date.min(), df_opp.date.max()]
    plt.style.use("seaborn")
    fig = plt.figure(figsize=(25, 8))
    fig.set_facecolor("white")
    fig.suptitle(f"Opportunities Report - {exec}\n ({date_range[0]} - {date_range[1]})", y=.98, fontsize=15, color="#17202A")
    gs = GridSpec(4, 4, hspace=.5)
    colors = ["#283747", "#5D6D7E", "#AEB6BF", "#F2F4F4"]
    
    
    #LINE PLOT
    ax = fig.add_subplot(gs[0, 0:4])
    ax.set_facecolor("white")
    ax.grid(b=False)
    df = opp_bydate.loc[opp_bydate["sales_rep_1"] == exec].sort_values(by="date", ascending=True)
    
    
    ax.plot(df["date"], df["opportunity"] , linewidth=3, color="#283747")
    # ax.plot(df_daily["Calls_ghost"], linewidth=3, label="Ghost", color="#9A6969")
    # ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
    # ax.set_facecolor("#D5D8DC")
    # ax.set_title(f"External calls - {start}-{end}", position=[.5, 1.25], fontsize=22)
    # ax.legend(fontsize=16)
    # ax.tick_params(axis="both", which="major", labelsize=15)
    
    #STACK BAR STATUS
    df1 = open_byrep.loc[open_byrep["sales_rep_1"] == exec].sort_values(by="count", ascending=True)
    ax1 = fig.add_subplot(gs[1, 0:3])
    ax1.set_yticklabels("")
    ax1.set_xticklabels("")
    ax1.set_facecolor("white")
    ax1.grid(b=False)
    
    widths = [0]
    widths += [i for i in df1["count"]]
    counter = 0
    # ax1.set_xlim(0, df1["count"].sum())
    ax1.set_ylim(0, 1.5)
    for val in widths[1:]:
        ax1.barh(1, val, height=.8, color=colors[counter], left=sum(widths[:counter+1]))
      
        counter += 1
        
    legends = [f"{df1.iloc[i]['status']}: {df1.iloc[i]['count']} ({round(df1.iloc[i]['count'] / df1['count'].sum() *100, 2)}%)" for i in range(len(df1))]
    ax1.legend(legends, loc="lower center", ncol=len(df1), bbox_to_anchor=(0.5, 0.1), fontsize=10)
    ax1.set_title(f"Open Opportunities", fontsize=13, loc="left")
     
    #STACK BAR OUTCOME
    df2 = won_byrep.loc[won_byrep["sales_rep_1"] == exec].sort_values(by="status", ascending=False)
    ax2 = fig.add_subplot(gs[2, 0:3])
    ax2.set_yticklabels("")
    ax2.set_xticklabels("")
    ax2.set_facecolor("white")
    ax2.grid(b=False)
   
    
    widths = [0]
    widths += [i for i in df2["count"]]
    counter = 0
    # ax2.set_xlim(0, df2["count"].sum())
    ax2.set_ylim(0, 1.5)
    for val in widths[1:]:
        ax2.barh(1, val, height=.8, color=colors[counter], left=sum(widths[:counter+1]))
        counter += 1
        
    legends = [f"{df2.iloc[i]['status'].split(' ')[1]}: {df2.iloc[i]['count']} ({round(df2.iloc[i]['count'] / df2['count'].sum() *100, 2)}%)" for i in range(len(df2))]
    ax2.legend(legends, loc="upper center", ncol=len(df2),  fontsize=10, bbox_to_anchor=(0.5, 0.4))
    ax2.set_title(f"Won/Lost Opportunities", fontsize=13, loc="left") 
    
    #TEXT
    ax3 = fig.add_subplot(gs[1:3, 3:])
    ax3.set_yticklabels("")
    ax3.set_xticklabels("")
    ax3.set_facecolor("white")
    ax3.grid(b=False)
    ax3.text(.5, .5, "na")
    
for exec in df_opp["sales_rep_1"].unique():
    graphing(exec)
    






