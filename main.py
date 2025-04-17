import pandas as pd
import matplotlib.pyplot as plt

def plot_spend_vs_points(csv_filename, title): #will eventually change to title automatically
    '''Plots yearly spending compared to points earned for a season'''
    data = pd.read_csv(csv_filename) #Data from .csv file
    data.columns = data.columns.str.strip() #Fixed KeyError
    print(data.head())

    data["Yearly_Spending"] = -data["Net_transfers"] + (data["Wages (weekly)"] * 52) #Combines transfer spending and weekly wages into yearly spending
    plt.figure(figsize=(14,7)) #Adjusts size
    plt.scatter(data["Yearly_Spending"], data["Points"])
    for i, row in data.iterrows():
        plt.text(row["Yearly_Spending"] + 1, row["Points"], row["Team"], fontsize=8) #Labels points
    plt.xlabel("Yearly Spend (€M)")
    plt.ylabel("League Points")
    plt.title(title)
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

plot_squadval_vs_points("EPL_Data.csv", "23-24")

'''
To do list:
    - Add data from more seasons
    - Create financial power score (normalize financial metrics and add)
    - Linear regressions for comparisons over seasons
    - pts return on squad value
    - tbd
'''