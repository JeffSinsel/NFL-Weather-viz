import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

#getting data from csv
clean = pd.read_csv("clean.csv")

#temperature
#getting a sample becasue the full data is hard to visualize
temperature_data = clean.sample(200)

#plotting the full scatter plot
y = temperature_data["total_score"]
x = temperature_data["temperature"]
sns.regplot(y=clean["total_score"],x=clean["temperature"])
plt.tight_layout()
plt.savefig("graphs/tempurature_full_scatter",dpi=300)
plt.show()

#testing the regression of the sample
r,pvalue = pearsonr(x, y)
a,b = np.polyfit(x,y,1)
sns.regplot(x=x,y=y,ci=0)

#printing results
print("For every degree warmer it is, the total score changes by",round(a,4),"with a p-value of",round(pvalue,4))
print("For example, the score of a 80 degree is expected to be",round(a*80+b,2),"and the score of a 40 degree game is expected to be",round(a*40+b,2))
#graphing results
plt.tight_layout()
plt.savefig("graphs/tempurature_sample_scatter",dpi=300)
plt.show()

#wind
#getting data from clean that has wind values
wind_data = clean[clean["wind"].notna()]
y = wind_data["total_score"]
x = wind_data["wind"]

#testing the regression
r,pvalue = pearsonr(x, y)
a,b = np.polyfit(x,y,1)
sns.regplot(x=x,y=y,ci=0)

#printing results
print("For every m/s faster the wind is is, the total score changes by",round(a,4),"with a p-value of",round(pvalue,4))
print("For example, the score of a game with 10 m/s winds is expected to be",round(a*10+b,2),"and the score of a game with 1 m/s winds is expected to be",round(a+b,2))
#graphing results
plt.tight_layout()
plt.savefig("graphs/wind_scatter",dpi=300)
plt.show()

#year
#getting data
x = clean['year']
y = clean['total_score']

#testing the regression
r,pvalue = pearsonr(x, y)
a,b = np.polyfit(x-2000,y,1)

#printing and graphing results
sns.boxplot(x=x,y=y)
plt.tight_layout()
plt.savefig("graphs/year_scatter",dpi=300)
plt.show()

#week
#getting data
x = clean['week']
y = clean['total_score']

#testing the regression
r,pvalue = pearsonr(x, y)
a,b = np.polyfit(x,y,1)

#printing and graphing results
sns.boxplot(x=x,y=y)
plt.tight_layout()
plt.savefig("graphs/week_scatter",dpi=300)
plt.show()

#fun graphs
#graphing box plot of home_teams vs home_score
sns.boxplot(x=clean['home_team'],y=clean['home_score'])
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("graphs/home_team_scoring_box",dpi=300)
plt.show()

#graphing box plot of wind_dir vs total_score
wind_dir_data = clean[clean["wind_dir"].notna()]
sns.boxplot(x=wind_dir_data["wind_dir"],y=wind_dir_data["total_score"],order=("N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"))
plt.tight_layout()
plt.savefig("graphs/wind_dir_box",dpi=300)
plt.show()