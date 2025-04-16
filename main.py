import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("EPL_Data.csv")
print(data.head())

plt.scatter(data["Net_transfers"], data["Points"])
plt.xlabel("Transfer Spend (€M)")
plt.ylabel("League Points")
plt.grid(True)
plt.show()
