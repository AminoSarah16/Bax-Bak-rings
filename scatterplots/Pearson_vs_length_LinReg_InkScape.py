import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file = "C:/Users/Sarah/Documents/Python/Bax-Bak-rings/results_all_clip.csv"
df = pd.read_csv(file, encoding='latin1')  # latin1 encocing needed in order to be able to read special chars like "µ"
print(df)

length = df['Length']
pearson = df['Pearson coefficient']


plt.figure(figsize=(12, 8))
plot = sns.regplot(x="Length", y="Pearson coefficient", data=df, scatter_kws={"color": "#808080", "s":3}, line_kws={"color": "#34e1eb", 'linewidth':1})

# wie weit soll die y axe gehen
plt.ylim(-1, 1)
# ich will nur alle 0.5 Einheiten einen Tickmark
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.5))

plt.xticks(fontsize=28, rotation=45)
plt.yticks(fontsize=28)
plt.plot()

# not needed for InkScape!
plt.show()