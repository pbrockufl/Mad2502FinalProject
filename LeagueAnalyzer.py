import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from adjustText import adjust_text

class LeagueAnalyzer:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.data.columns = self.data.columns.str.strip()
        self.models = {} #Dictionary that stores models

    def filter_seasons(self, start_season, end_season):
        '''filters season range'''
        self.filtered_data = self.data[
            (self.data["Season"] >= start_season) & (self.data["Season"] <= end_season)].copy()
        self.start_season = start_season
        self.end_season = end_season

    def compute_yearly_spending(self):
        '''Calculates a club's yearly spending'''
        self.filtered_data["Yearly_Spending"] = -self.filtered_data["Net_transfers"] + (self.filtered_data["Wages (weekly)"] * 52)

    def plot_spend_vs_points(self):
        '''Plots yearly spending compared to points earned for a season'''
        self.compute_yearly_spending()

        #Sum spending and average points
        total_data = self.filtered_data.groupby("Team").agg({
            "Yearly_Spending": "sum",
            "Points": "mean"
        }).reset_index()
        # Scatterplot
        plt.figure(figsize=(14, 7))  # Adjusts size
        plt.scatter(total_data["Yearly_Spending"], total_data["Points"])

        # Point labels
        texts = []
        for i, row in total_data.iterrows():
            texts.append(
                plt.text(row["Yearly_Spending"] + 1, row["Points"], row["Team"], fontsize=8)  # Labels points
            )
        adjust_text(texts, arrowprops=dict(arrowstyle="-", color="gray"))  # Uses AdjustText to make labels readable

        # Regression
        x = total_data["Yearly_Spending"].values.reshape(-1, 1)
        y = total_data["Points"].values
        model = LinearRegression()
        model.fit(x, y)
        prediction = model.predict(x)
        # plot regression
        plt.plot(total_data["Yearly_Spending"], prediction, color="blue", linestyle="--", label="Regression Line")
        # equation
        slope = model.coef_[0]
        intercept = model.intercept_ # Y intercept
        r2 = model.score(x, y) # Represents correlation
        equation = f"Points = {slope:.2f} * Spending + {intercept:.2f}\nr^2 = {r2:.4f}"
        plt.text(
            0.05, 0.95, equation,
            transform=plt.gca().transAxes, # Everything placed inside axes
            fontsize=12,
            verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")
        )

        # Decorations
        plt.xlabel("Total Yearly Spend (€M) Across Seasons")
        plt.ylabel("Average League Points Across Seasons")
        plt.title(f"EPL {self.start_season}-{self.end_season}: Spending vs. Points")
        plt.grid(True)
        plt.show()

    def plot_squadval_vs_points(self):
        '''Plots squad value compared to points'''
        averaged = self.filtered_data.groupby("Team").agg({
            "Squad_value":"mean",
            "Points":"mean"
        }).reset_index()

        # Scatterplot
        plt.figure(figsize=(14, 7))
        plt.scatter(averaged["Squad_value"], averaged["Points"])
        texts = []

        # Labels
        for i, row in averaged.iterrows():
            texts.append(plt.text(row["Squad_value"] + 1, row["Points"], row["Team"], fontsize=8))
        adjust_text(texts, arrowprops=dict(arrowstyle="-", color="gray"))  # Uses AdjustText to make labels readable

        # Regression Line
        x = averaged["Squad_value"].values.reshape(-1, 1)
        y = averaged["Points"].values
        model = LinearRegression()
        model.fit(x, y)
        predictions = model.predict(x)
        # plot regression
        plt.plot(averaged["Squad_value"], predictions, color="blue", linestyle="--", label="Regression Line")
        # equation
        slope = model.coef_[0]
        intercept = model.intercept_
        r2 = model.score(x, y)
        equation = f"Points = {slope:.2f} * Squad Value + {intercept:.2f}\nr^2 = {r2:.4f}"
        plt.text(
            0.05, 0.95, equation,
            transform=plt.gca().transAxes,
            fontsize=12,
            verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")
        )

        # Decorations
        plt.xlabel("Average Squad Value (€M)")
        plt.ylabel("Average League Points")
        plt.title(f"EPL {self.start_season}-{self.end_season}: Squad Value vs. Points")
        plt.grid(True)
        plt.show()

    def compare_power_points(self):
        '''Compares power points of EPL clubs vs clubs from other top 5 leagues'''
        # Group leagues
        league_avg = self.data.groupby("League")["Power_points"].mean().sort_values(ascending=False)
        colors = {
            "EPL": "purple",
            "La Liga": "yellow",
            "Bundesliga": "red",
            "Serie A": "green",
            "Ligue 1": "blue"
        }

        graph_colors = [colors.get(league, "gray") for league in league_avg.index]
        # plot
        plt.figure(figsize=(10, 6))
        bars = plt.bar(league_avg.index, league_avg.values, color=graph_colors, edgecolor="black")

        # Labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.01, f"{height:.2f}",
                     ha="center", va="bottom", fontsize=10)

        # Decorations
        plt.ylabel("Average Power Points")
        plt.title("Average Power Points across Top 5 Leagues")
        plt.xticks(rotation=45)
        plt.grid(True, axis="y")
        plt.tight_layout()
        plt.show()

    def predict_points_from_spend(self, spend_amount):
        '''Predicts points based on spending from model'''
        if "spending" not in self.models:
            print("Run plot_spend_vs_points() first.") # Warns if model not available
            return None
        prediction = self.models["spending"].predict([[spend_amount]])[0]
        return prediction

    def predict_points_from_squad_value(self, squad_value):
        '''Predicts points based on squad value from model'''
        if "squad_value" not in self.models:
            print("Run plot_squadval_vs_points() first.")
            return None
        prediction = self.models["squad_value"].predict([[squad_value]])[0]
        return prediction

    def compare_spending_power(self, league1, league2):
        '''Compares net spend and UCL points between two leagues'''
        #Filter out teams not in UCL and leagues
        filtered = self.data[self.data["UCL Points"] > 0].copy()
        data1 = filtered[filtered["League"] == league1]
        data2 = filtered[filtered["League"] == league2]

        #Scatterplot
        plt.figure(figsize=(14, 7))
        plt.scatter(data1["Net Spend (€M)"], data1["UCL Points"], color = "blue", label=league1, edgecolor="black")
        plt.scatter(data2["Net Spend (€M)"], data1["UCL Points"], color = "red", label=league2, edgecolor="black")

        #League 1 Regression
        x1 = data1["Net Spend (€M)"].values.reshape(-1,1)
        y1 = data1["UCL Points"].values
        model1 = LinearRegression()
        model1.fit(x1, y1)
        prediction1 = model1.predict(x1)
        plt.plot(data1["Net Spend (€M)"], prediction1, color="blue", linestyle="--")

        #League 2 Regression
        x2 = data2["Net Spend (€M)"].values.reshape(-1, 1)
        y2 = data2["UCL Points"].values
        model2 = LinearRegression()
        model2.fit(x2, y2)
        prediction1 = model1.predict(x2)
        plt.plot(data2["Net Spend (€M)"], prediction1, color="red", linestyle="--")

        #Equation
        slope1 = model1.coef_[0]
        intercept1 = model1.intercept_
        r2_1 = model1.score(x1, y1)

        slope2 = model2.coef_[0]
        intercept2 = model2.intercept_
        r2_2 = model2.score(x2, y2)

        eq1 = f"{league1}: y = {slope1:.2f}x + {intercept1:.2f}\nr^2 = {r2_1:.4f}"
        eq2 = f"{league2}: y = {slope2:.2f}x + {intercept2:.2f}\nr^2 = {r2_2:.4f}"

        plt.text(0.05, 0.95, eq1,
            transform=plt.gca().transAxes,
            fontsize=12,
            verticalalignment="top", color ="blue",
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="blue", facecolor="white"))
        plt.text(0.05, 0.75, eq2,
            transform=plt.gca().transAxes,
            fontsize=12,
            verticalalignment="top", color = "red",
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="red", facecolor="white"))
        #Results
        print(f"{league1}: slope = {slope1:.4f}, r^2 = {r2_1:.4f}")
        print(f"{league2}: slope = {slope2:.4f}, r^2 = {r2_2:.4f}")

        if slope1 > slope2:
            print(f"Spending is more powerful in {league1}.")
        else:
            print(f"Spending is more powerful in {league2}.")

        #Decorations
        plt.xlabel("Net Transfer Spend (€M)")
        plt.ylabel("UCL Points")
        plt.title(f"Spending vs UCL Success: {league1} vs {league2}")
        plt.legend
        plt.grid(True)
        plt.tight_layout()
        plt.show()

