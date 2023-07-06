import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from pandas import DataFrame

def getCorr(data, x, y):

    cor_data = data.loc[data[x].notnull() & data[y].notnull()]

    corr, _ = pearsonr(x=cor_data[x], y=cor_data[y])

    label = f"`{x}` and `{y}` pearson's correlation: {round(corr, 3)}"

    return label

def plotScatter(
    data: DataFrame,
    x: str,
    y: str,
    marker: str = "Country Name"
) -> None:

    """
    Print Pearson Correlation and plot graph
    """
    label = getCorr(data, x, y)

    # Prepare Scatter Plot
    pl = sns.scatterplot(data=data, x=x, y=y)
    pl.set(title=label)

    # Append the Countries Names
    for line in range(0,data.shape[0]):
        pl.text(
            data.iloc[line][x]+0.01,
            data.iloc[line][y],
            data.iloc[line][marker],
            horizontalalignment='left',
            size='medium',
            color='black',
            weight='semibold')

    plt.show()


x = "Investment in tourism"
y = "Number of arrivals"
z = "Number of departures"

# Without filtering
data = df

# Filtering by region and the year 2018
loc = ((~df['is_region']) & # Not a region
    (df['Year'] == '2018')) # Recent data
data=df.loc[loc]

# Plot correlation between investment and number of arrivals
getCorr(data, y, z)
plotScatter(data=data, x=y, y=z)

# Plot correlation between investment and number of arrivals
getCorr(data, x, y)
plotScatter(data=data, x=x, y=y)

# Plot correlation between investment and number of arrivals
getCorr(data, x, y)
plotScatter(data=data, x=x, y=z)

# Principal component analysis
from pca import pca

X = df.loc[loc][[x, y, z]]
X = X.loc[X[x].notnull() & X[y].notnull() & X[z].notnull()]

# Number of components are extracted that cover at least 95% of the explained variance.
model = pca(n_components=2)

# Fit transform
results = model.fit_transform(X)

# Cumulative explained variance
print(model.results['explained_var'])
# [0.92461872 0.97768521 0.99478782]

# Explained variance per PC
print(model.results['variance_ratio'])

# Make plot
fig, ax = model.plot()
fig.show()

fig, ax = model.biplot(n_feat=3, PC=[0,1], legend=True)
fig.show()
# 1 PC explains 99% of the variance