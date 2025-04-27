import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from adjustText import adjust_text

class LeagueAnalyzer:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.data.columns = self.data.columns.str.strip()
        self.models = {}

    def filter_seasons(self, start_season, end_season):
        self.filtered_data = self.data[
            (self.data["Season"] >= start_season) & (self.data["Season"] <= end_season)].copy()
        self.start_season = start_season
        self.end_season = end_season

    def compute_yearly_spending(self):
        self.filtered_data["Yearly_Spending"] = -self.filtered_data["Net_transfers"] + (self.filtered_data["Wages (weekly)"] * 52)

    def plot_spend_vs_points(self):
        self.compute_yearly_spending()

        #Sum spending and average points
        total_data = self.filtered_data.groupby("Team").agg({
            "Yearly_Spending": "sum",
            "Points": "mean"
        })
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
        intercept = model.intercept_
        r2 = model.score(x, y)
        equation = f"Points = {slope:.2f} * Spending + {intercept:.2f}\nr^2 = {r2:.4f}"
        plt.text(
            0.05, 0.95, equation,
            transform=plt.gca().transAxes,
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

