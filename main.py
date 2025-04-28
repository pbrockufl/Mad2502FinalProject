from LeagueAnalyzer import LeagueAnalyzer

# Premier League analysis
EPL_analyzer = LeagueAnalyzer("EPL_Data.csv")
EPL_analyzer.filter_seasons(2020, 2023)
EPL_analyzer.plot_spend_vs_points()
EPL_analyzer.plot_squadval_vs_points()
EPL_analyzer.predict_points_from_spend(500)  # Predict points if spending 500M
EPL_analyzer.predict_points_from_squad_value(1000)  # Predict points with 1B squad value

# Europe-wide analysis
Top5_analyzer = LeagueAnalyzer("Top_5_Data.csv")
Top5_analyzer.compare_power_points()
Top5_analyzer.compare_spending_power("EPL", "La Liga")