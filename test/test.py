import matplotlib.pyplot as plt
import seaborn as sns

def plotScatter(data, x, y, marker):
    pl = sns.scatterplot(data=data, x=x, y=y)
    for line in range(0,data.shape[0]):
        pl.text(
            data.iloc[line][x]+0.01,
            data.iloc[line][y],
            data.iloc[line][marker],
            horizontalalignment='left',
            size='medium', color='black', weight='semibold')
    plt.show()

data=df.loc[
    ((~df['is_region']) & # Not a region
    (df['Year'] == '2018')) # Recent data
]

# Plot correlation between investment and number of arrivals
plotScatter(
    data=data,
    x="Investment in tourism",
    y="Number of arrivals",
    marker="Country Name")

# Plot correlation between investment and number of arrivals
plotScatter(
    data=data,
    x="Investment in tourism",
    y="Number of departures",
    marker="Country Name")

# Plot correlation between investment and number of arrivals
plotScatter(
    data=data,
    x="Number of arrivals",
    y="Number of departures",
    marker="Country Name")

