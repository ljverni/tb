import pandas as pd
from datetime import datetime
import calendar
import numpy as np
from datetime import date, timedelta
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

current_month = date.today().replace(day=1).strftime("%B") #currenty month
previous_month = (date.today().replace(day=1) - timedelta(1)).strftime("%B") #previous month
# next_month = (date.today().replace(day=1) + timedelta(1)).strftime("%B") #next month


#DF CLEANING######################################
df_opp.columns = df_opp.columns.str.lower().str.replace(" ", "_")
df_opp.rename(columns={"projected_total": "gp", "sales_rep": "sales_rep_2", "opportunity_status": "status"}, inplace=True)

def clean_gp():
    for symbol in [",", "(", ")"]: #remove symbols from amount
        df_opp["gp"] = df_opp["gp"].apply(lambda x: (x.replace(symbol, ""))) 
    df_opp["gp"] = df_opp["gp"].astype(float)
clean_gp()

df_opp["date"] = df_opp["date"].apply(lambda x: datetime.strptime(x, "%d/%m/%Y")) #drop 2021
df_opp.drop(df_opp.loc[df_opp["date"].dt.year == 2020].index, inplace=True)
df_opp["month"] = df_opp["date"].apply(lambda x: x.strftime("%B")) #add month col
df_opp["date"] = df_opp["date"].apply(lambda x: x.date())

df_opp.replace("Lost Customer", "Closed", inplace=True) #replace status
df_opp.replace("Closed Lost", "Closed", inplace=True) #replace status
df_opp.replace("Closed Won", "Won", inplace=True) #replace status

df_opp.loc[df_opp["sales_rep_2"].isna(), "sales_rep_2"] = df_opp.loc[df_opp["sales_rep_2"].isna(), "sales_rep_1"] #remove nan from rep
df_opp.loc[df_opp["sales_rep_1"].isna(), "sales_rep_1"] = df_opp.loc[df_opp["sales_rep_1"].isna(), "sales_rep_2"] #remove nan from rep1

df_opp["sales_rep_2"] = df_opp["sales_rep_2"].apply(lambda x: x.split(" ", 1)[1]) #removing id from rep
df_opp["sales_rep_1"] = df_opp["sales_rep_1"].apply(lambda x: x.split(" ", 1)[1]) #removing id from rep1

df_opp["title"].replace(np.nan, "No title", inplace=True) #replace nan titles

df_opp.drop(df_opp.loc[~df_opp["sales_rep_1"].isin(rep_dict.keys())].index, inplace=True) #drop non end user team

#ANALYTICS#####################################

#OPEN DF
open_byrep = df_opp.loc[(df_opp["status"] != "Won") & (df_opp["status"] != "Closed") & (df_opp["status"] != "Closed")].groupby(by=["sales_rep_1", "status", "month"], as_index=False).agg({"date": "count", "gp": "sum"}).rename(columns={"date": "count"})
open_total = open_byrep.groupby(by=["status", "month"], as_index=False).agg({"gp": "sum", "count": "sum"})
open_total["sales_rep_1"] = "Total"
open_byrep = pd.concat([open_byrep, open_total], ignore_index=True)

#WON DF
won_byrep = df_opp.loc[(df_opp["status"] == "Won") | (df_opp["status"] == "Closed") | (df_opp["status"] == "Closed")].groupby(by=["sales_rep_1", "status", "month"], as_index=False).agg({"date": "count", "gp": "sum"}).rename(columns={"date": "count"})
won_total = won_byrep.groupby(by=["status", "month"], as_index=False).agg({"gp": "sum", "count": "sum"})
won_total["sales_rep_1"] = "Total"
won_byrep = pd.concat([won_byrep, won_total], ignore_index=True)


#OPP REP DF
opp_byrep = df_opp.groupby(by=["sales_rep_1", "month"], as_index=False).agg({"customer": "count", "gp": "sum"}).rename(columns={"customer": "opportunity"})
opp_bymonth = df_opp.groupby(by="month", as_index=False).agg({"customer": "count", "gp": "sum"}).rename(columns={"customer": "opportunity"})
opp_bymonth["sales_rep_1"] = "Total"
opp_byrep = pd.concat([opp_byrep, opp_bymonth], ignore_index=True)


def graphing(exec):
    colors = ["#283747", "#5D6D7E", "#AEB6BF", "#BFC9CA", "#F2F4F4"] #colors
    
    #FUNTIONS
    def plotter(ax):
        ax.set_yticklabels("")
        ax.set_xticklabels("")
        ax.set_facecolor("white")
        ax.grid(b=False)
    
    #DF 
    df_open = open_byrep.loc[(open_byrep["sales_rep_1"] == exec) & (open_byrep["month"] == current_month)].sort_values(by="count", ascending=True)
    df_won = won_byrep.loc[(won_byrep["sales_rep_1"] == exec) & (won_byrep["month"] == current_month)].sort_values(by="status", ascending=False)
    df_byrep = opp_byrep.loc[opp_byrep["sales_rep_1"] == exec]

    #CREATE FIGURE
    plt.style.use("seaborn")
    fig = plt.figure(figsize=(25, 8))
    fig.suptitle(f"Forecast Report - {exec}\n ({current_month})", y=.9, fontsize=15, color="#17202A")
    gs = GridSpec(4, 4, hspace=.5)
    
    
    #STACK BAR STATUS
    ax1 = fig.add_subplot(gs[2, 0:2])
    plotter(ax1)
    
    widths = [0]
    widths += [i for i in df_open["count"]]
    counter = 0
    
    if df_open["count"].sum() > 0:
        for val in widths[1:]:
            ax1.barh(1, val, height=.8, color=colors[counter], left=sum(widths[:counter+1]))
            counter += 1
        ax1.set_xlim(0, df_open["count"].sum())
        ax1.set_ylim(0, 1.5)
        legends = [f"{df_open.iloc[i]['status']}: {df_open.iloc[i]['count']} ({round(df_open.iloc[i]['count'] / df_open['count'].sum() *100, 2)}%)" for i in range(len(df_open))] #legend
    
        if len(legends) > 3:
            legend_vert = -.15
        else:
            legend_vert = .05
        
        ax1.legend(legends, loc="lower center", ncol=3, bbox_to_anchor=(.5, legend_vert), fontsize=10)
        ax1.set_title(f"Open Opportunities", fontsize=13, loc="left")
     
    
    #STACK BAR OUTCOME
    ax2 = fig.add_subplot(gs[3, 0:2])
    plotter(ax2)
 
    widths = [0]
    widths += [i for i in df_won["count"]]
    counter = 0
    
    if len(df_won) > 0:
        if len(widths) > 2:
            for val in widths[1:]:
                ax2.barh(1, val, height=.8, color=colors[counter], left=sum(widths[:counter+1]))
                ax2.set_xlim(0, df_won["count"].sum())
                ax2.set_ylim(0, 1.5)
                counter += 1
        elif len(widths) == 2:
            ax2.barh(1, df_won["count"].values[0], height=.8, color=colors[0])
            ax2.set_xlim(0, df_won["count"].sum())
            ax2.set_ylim(0, 1.5)
            
        legends = [f"{df_won.iloc[i]['status']}: {df_won.iloc[i]['count']} ({round(df_won.iloc[i]['count'] / df_won['count'].sum() *100, 2)}%)" for i in range(len(df_won))]
        ax2.legend(legends, loc="upper center", ncol=len(df_won),  fontsize=10, bbox_to_anchor=(0.5, 0.4))
        ax2.set_title(f"Won/Lost Opportunities", fontsize=13, loc="left") 
        
    #TEXT
    ax3 = fig.add_subplot(gs[1, 0:2])
    plotter(ax3)
    ax3.set_ylim(0, 1)
    
    if len(df_byrep["opportunity"]) > 0:
        total_opp = df_byrep["opportunity"].values[0]
    else:
        total_opp = 0
    if len(df_won.loc[df_won["status"] == "Won"]["count"]) > 0:
        opp_won = df_won.loc[df_won["status"] == "Won"]["count"].values[0]
    else:
        opp_won = 0
    if len(df_won.loc[df_won["status"] == "Closed"]["count"]) > 0:
        opp_lost = df_won.loc[df_won["status"] == "Closed"]["count"].values[0]
    else:
        opp_lost = 0
    if df_open["count"].sum() > 0:
        opp_open = df_open["count"].sum()
    else:
        opp_open = 0
    
    if
    total_gp = "{:,}".format(int(df_byrep["gp"].values[0]))
    gp_won =  "{:,}".format(int(df_won.loc[df_won["status"] == "Won"]["gp"].values[0]))
    gp_lost = "{:,}".format(int(df_won.loc[df_won["status"] == "Closed"]["gp"].values[0]))
    gp_open = "{:,}".format(int(df_open["gp"].sum()))
    
    # if opp_won == 0:
    #     won_perc = 0
    # else:
    #     won_perc = int(opp_won / total_opp * 100)
        
    # if opp_lost == 0:
    #     lost_perc = 0
    # else:
    #     lost_perc = int(opp_lost / total_opp * 100)
    
    # tot_lst= {total_opp: "Total Opportunities", opp_open: "Open Opportunities", f"£{total_gp}": "Last Month Profit", f"£{total_gp}": "Current Month Profit", f"{won_perc}%": "Won Opportunities", f"{lost_perc}%": "Lost Opportunities"}
              
    # hlocs = [.2, .2, .5, .5, .8, .8]
    # vlocs = [1.4, .6, 1.4, .6, 1.4, .6]
    
    
    # for i in range(len(tot_lst)):
    #     ax3.text(hlocs[i], vlocs[i], list(tot_lst)[i], verticalalignment="center", horizontalalignment="center", color="#283747", fontsize=17, weight="bold")
    #     ax3.text(hlocs[i], vlocs[i]-0.2, tot_lst[list(tot_lst)[i]], verticalalignment="center", horizontalalignment="center", color="#17202A", fontsize=12.5)


    # ax4 = fig.add_subplot(gs[0, 3:5])
    # ax4.set_yticklabels("")
    # ax4.set_xticklabels("")
    # ax4.set_facecolor("white")
    # ax4.grid(b=False)   
    
    # ax5 = fig.add_subplot(gs[0, :])
    # ax5.set_yticklabels("")
    # ax5.set_xticklabels("")
    # ax5.set_facecolor("white")
    # ax5.axline([-1, .5], [1, .5], color="#283747", linewidth=10, alpha= .5)
    # ax5.set_ylim(0, 1)
    # ax5.grid(b=False)   
    

# C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\fig\opportunities
    



for exec in open_byrep["sales_rep_1"].unique():
    graphing(exec)
    


