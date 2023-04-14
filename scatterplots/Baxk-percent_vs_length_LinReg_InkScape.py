import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file=f"C:/Users/Sarah/Nextcloud/Bax-Bak-ring_analysis/results_all.csv"
df = pd.read_csv(file, encoding='latin1')

length = df['Length']
Bak_percent = df['Percent Bak']
Bax_percent = df['Percent Bax']


plt.figure(figsize=(12, 8))
plot = sns.regplot(x=length, y=Bax_percent, data=df, scatter_kws={"color": "#808080", "s":20}, line_kws={"color": "#34e1eb", 'linewidth':1})

# wie weit soll die y axe gehen
plt.ylim(0, 100)

#adjust size again down below
plt.xticks(fontsize=28, rotation=45)
plt.yticks(fontsize=28)


#second y axis für Bax
ax2 = plt.twinx()
plot2 = sns.regplot(x=length, y=Bak_percent, data=df, ax=ax2, scatter_kws={"color": "#808080", "s":20}, line_kws={"color": "#34e1eb", 'linewidth':1})
plt.ylim(100, 0)

plt.xticks(fontsize=28)
plt.yticks(fontsize=28)

#keine Axis labels
plot.set(xlabel=None)
plot.set(ylabel=None)
plot2.set(ylabel=None)


plt.plot()

# not needed for InkScape!
plt.show()
