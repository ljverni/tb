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

turnover = pd.read_csv(r"C:\Users\l.verni\Documents\Local-Repo\analytics\eu_master\data\Customers452.csv", usecols=["Turnover", "ID"], dtype=str)

turnover["Turnover"] = turnover["Turnover"].apply(lambda x: x[0: len(x)-4].replace(",", ""))

turnover["Turnover"] = turnover["Turnover"].astype(float)
turnover = turnover.drop(turnover.loc[turnover["Turnover"] == 0].index)
# turnover = turnover.astype(int)

turnover.to_excel("turnovers.xlsx")

turn_array = turnover["Turnover"].unique()


grade_a = np.quantile(turn_array, .75)
grade_b = np.quantile(turn_array, .5)
grade_c = np.quantile(turn_array, .25)

df_a = turnover.loc[turnover["Turnover"] > grade_a]
df_b = turnover.loc[(turnover["Turnover"] < grade_a) & (turnover["Turnover"] > grade_c)]
df_c = turnover.loc[turnover["Turnover"] < grade_c]

num_a = df_a.count()[0]
num_b = df_b.count()[0]
num_c = df_c.count()[0]
million = 1000000
range_a = f"more than {df_a.min()[0]/million}"
range_b = f"{df_b.min()[0]/million} to {df_b.max()[0]/million}"
range_c = f"Less than {df_c.max()[0]/million}"

print("There are " + str(num_a) + " with a turnover of more than " + range_a)

plt.style.use("seaborn")
fig = plt.figure(figsize=(10, 2))
fig.set_facecolor("white")
fig.suptitle(f"Customers grading by turnover")
gs = GridSpec(1, 1)
ax = fig.add_subplot(gs[0, 0])
ax.set_xticks([grade_c, grade_b, grade_a])
ax.set_xticklabels(["C", "B", "A"])
ax.set_facecolor("white")
ax.grid(b=False)


sns.boxplot(x=turn_array, showfliers=False)


# ax3.set_title("Ratios - Weekend (UK)", position=[.5, 1.25], fontsize=18)

# ax3.artists[0].set_facecolor("#7796B4")
# ax3.artists[1].set_facecolor("#5A6C7E")
# ax3.artists[2].set_facecolor("#33608B")
# ax3.tick_params(axis="x", which="major", labelsize=15)