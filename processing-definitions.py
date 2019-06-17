#%% [markdown]
# ## Processing definitions collected from professors and students
# ### Ehsan Moradi, Ph.D. Candidate

#%% [markdown]
# ### Load required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import re
import operator

plt.rcParams["axes.grid"] = True

#%% [markdown]
# ### Loading observations from Excel into a pandas dataframe
directory = r"/Users/ehsan/Dropbox/Academia/Sustainability Definition Project"
file = r"/professors_responses.xlsx"
path = directory + file
df = pd.read_excel(path, sheet_name="Sheet1")

#%% [markdown]
# ### Cleaning up sentences by removing signs, quotations, commas, points, etc.
vectors = np.array([])
for i in range(len(df)):
    sentence = df["sentence"][i]
    result = re.findall(r"((\b[^\s]+\b)((?<=\.\w).)?)", sentence)
    vectors = np.append(vectors, np.array([x[0] for x in result]))

#%% [markdown]
# ### Make a dictionary with words as keys and counts as values, then sort the dictionary based on counts
words = pd.DataFrame()
words["word"], words["count"] = np.unique(vectors, return_counts=True)
words = words.sort_values(by=["count"], ascending=False)

#%% [markdown]
# ### Plotting a histogram
x = words["word"]
y = words["count"]
fig = plt.figure(figsize=(25, 10))
gs = gridspec.GridSpec(1, 1, figure=fig)
gs.tight_layout(fig)
ax = fig.add_subplot(gs[0])
ax.bar(x[:50], y[:50], color="SkyBlue")
fig.autofmt_xdate()
plt.show()

#%% [markdown]
# ### Add results back to the Excel file
directory = r"/Users/ehsan/Dropbox/Academia/Sustainability Definition Project"
file = r"/output.xlsx"
path = directory + file
words.to_excel(path, sheet_name="professors")
