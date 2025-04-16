import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("EPL_Data.csv")
print(data.head())

plt.figure(figsize=(10,6))
plt.scatter(data["Net_transfers"], data["Points"])
for i, row in data.iterrows():
    plt.text(row["Net_transfers"] + 1, row["Points"], row["Team"])
plt.xlabel("Transfer Spend (€M)")
plt.ylabel("League Points")
plt.title("EPL 23-24")
plt.grid(True)
plt.show()
