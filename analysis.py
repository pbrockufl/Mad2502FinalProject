import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text
from sklearn.linear_model import LinearRegression
import numpy as np

def plot_spend_vs_points(csv_filename, start_season, end_season): #will eventually change to title automatically
    '''Plots yearly spending compared to points earned for a season'''
    data = pd.read_csv(csv_filename) #Data from .csv file
    data.columns = data.columns.str.strip() #Fixed KeyError
    data["Season"] = data["Season"].astype(int) #Season into int

    #Filter
    season_range = data[(data["Season"] >= start_season) & (data["Season"] <= end_season)]
    season_range["Yearly_Spending"] = -season_range["Net_transfers"] + (season_range["Wages (weekly)"] * 52)

    #Sum spending and average points
    total_data = season_range.groupby("Team").agg({
        "Yearly_Spending": "sum", #sums spending over season
        "Points": "mean", #averages points over season
    }).reset_index()

    #Scatterplot
    plt.figure(figsize=(14,7)) #Adjusts size
    plt.scatter(total_data["Yearly_Spending"], total_data["Points"])

    #Point labels
    texts = []
    for i, row in total_data.iterrows():
        texts.append(
            plt.text(row["Yearly_Spending"] + 1, row["Points"], row["Team"], fontsize=8) #Labels points
        )
    adjust_text(texts, arrowprops=dict(arrowstyle="-", color="gray")) #Uses AdjustText to make labels readable

    #Regression
    x = total_data["Yearly_Spending"].values.reshape(-1,1)
    y = total_data["Points"].values
    model = LinearRegression()
    model.fit(x,y)
    prediction = model.predict(x)
    #plot regression
    plt.plot(total_data["Yearly_Spending"], prediction, color="blue",linestyle="--", label = "Regression Line")
    #equation
    slope = model.coef_[0]
    intercept = model.intercept_
    equation = f"Points = {slope:.2f} * Spending + {intercept:.2f}"
    plt.text(
        0.05, 0.95, equation,
        transform=plt.gca().transAxes,
        fontsize=12,
        verticalalignment = "top",
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")
    )
    #Decorations
    plt.xlabel("Total Yearly Spend (€M) Across Seasons")
    plt.ylabel("Average League Points Across Seasons")
    plt.title(f"EPL {start_season}-{end_season}: Spending vs. Points")
    plt.grid(True)
    plt.show()

def plot_squadval_vs_points(csv_filename, start_season, end_season):
    '''Plots squad value compared to points'''
    data = pd.read_csv(csv_filename)
    data.columns = data.columns.str.strip()
    data["Season"] = data["Season"].astype(int)
    #Filter
    season_range = data[(data["Season"] >= start_season) & (data["Season"] <= end_season)]
    averaged = season_range.groupby("Team").agg({
        "Squad_value": "mean",
        "Points": "mean"
    }).reset_index()

    #Scatterplot
    plt.figure(figsize=(14,7))
    plt.scatter(averaged["Squad_value"], averaged["Points"])
    texts = []

    #Labels
    for i, row in averaged.iterrows():
        texts.append(plt.text(row["Squad_value"] + 1, row["Points"], row["Team"], fontsize=8))
    adjust_text(texts, arrowprops=dict(arrowstyle="-", color="gray")) #Uses AdjustText to make labels readable

    #Regression Line
    x = averaged["Squad_value"].values.reshape(-1,1)
    y = averaged["Points"].values
    model = LinearRegression()
    model.fit(x,y)
    predictions = model.predict(x)

    plt.plot(averaged["Squad_value"], predictions, color="blue", linestyle="--", label="Regression Line")

    #Coeffs
    slope = model.coef_[0]
    intercept = model.intercept_

    equation = f"Points = {slope:.2f} * Squad Value + {intercept:.2f}"
    plt.text(
        0.05, 0.95, equation,
        transform=plt.gca().transAxes,
        fontsize = 12,
        verticalalignment = "top",
        bbox = dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")
    )

    #Decorations
    plt.xlabel("Average Squad Value (€M)")
    plt.ylabel("Average League Points")
    plt.title(f"EPL {start_season}-{end_season}: Squad Value vs. Points")
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