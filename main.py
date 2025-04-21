import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

def plot_spend_vs_points(csv_filename, start_season, end_season): #will eventually change to title automatically
    '''Plots yearly spending compared to points earned for a season'''
    data = pd.read_csv(csv_filename) #Data from .csv file
    data.columns = data.columns.str.strip() #Fixed KeyError
    data["Season"] = data["Season"].astype(int) #Season into int

    season_range = data[(data["Season"] >= start_season) & (data["Season"] <= end_season)]
    season_range["Yearly_Spending"] = -season_range["Net_transfers"] + (season_range["Wages (weekly)"] * 52)

    total_data = season_range.groupby("Team").agg({ #averages values over selected seasons
        "Yearly_Spending": "sum",
        "Points": "sum",
    }).reset_index()

    #data["Yearly_Spending"] = -data["Net_transfers"] + (data["Wages (weekly)"] * 52) #Combines transfer spending and weekly wages into yearly spending
    plt.figure(figsize=(14,7)) #Adjusts size
    #plt.scatter(data["Yearly_Spending"], data["Points"])
    plt.scatter(total_data["Yearly_Spending"], total_data["Points"])

    texts = []
    for i, row in total_data.iterrows():
        texts.append(
            plt.text(row["Yearly_Spending"] + 1, row["Points"], row["Team"], fontsize=8) #Labels points
        )
    adjust_text(texts, arrowprops=dict(arrowstyle="-", color="gray")) #Uses AdjustText to make labels readable
    plt.xlabel("Total Yearly Spend (€M) Across Seasons")
    plt.ylabel("Total League Points Across Seasons")
    plt.title(f"EPL {start_season}-{end_season}: Spending vs. Points")
    plt.grid(True)
    plt.show()

def plot_squadval_vs_points(csv_filename, title):
    '''Plots squad value compared to points'''
    data = pd.read_csv(csv_filename)
    data.columns = data.columns.str.strip()
    print(data.head())

    plt.figure(figsize=(14,7))
    plt.scatter(data["Squad_value"], data["Points"])
    for i, row in data.iterrows():
        plt.text(row["Squad_value"] + 1, row["Points"], row["Team"], fontsize=8)
    plt.xlabel("Squad Value (€M)")
    plt.ylabel("League Points")
    plt.title(title)
    plt.grid(True)
    plt.show()



'''
To do list:
    - Add data from more seasons
    - Create financial power score (normalize financial metrics and add)
    - Linear regressions for comparisons over seasons
    - pts return on squad value
    - tbd
'''

plot_spend_vs_points("EPL_Data.csv", 2020, 2023)