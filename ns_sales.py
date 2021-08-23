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

df_sales = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\TBLSalesOrdersViewLucUKResults133.csv", usecols=["Date", "Order", "Name", "Sales Rep", "Primary Customer Category", "Est. Gross Profit (Transaction)"])

# df_sales_original = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\TBLSalesOrdersViewLucUKResults133.csv")

df_sales.columns = df_sales.columns.str.lower().str.replace(" ", "_")
df_sales.rename(columns={"order": "so", "est._gross_profit_(transaction)": "gp", "primary_customer_category": "category"}, inplace=True)

for symbol in [",", "(", ")"]: #remove symbols from amount
    df_sales["gp"] = df_sales["gp"].apply(lambda x: (x.replace(symbol, ""))) 
df_sales["gp"] = df_sales["gp"].astype(float)


df_sales["sales_rep"] = df_sales["sales_rep"].apply(lambda x: x.split(" ", 1)[1])
df_sales["so"] = df_sales["so"].apply(lambda x: x.split(" ")[-1][1:])

print(df_sales.loc[df_sales["so"] == "SO158656"])