from sklearn.metrics import brier_score_loss
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

gpt_data = pd.read_csv("data.csv", usecols=[' zeroGPT Confidence'])
ground_truth = pd.read_csv("../furtherAIDetectionResearch/AI_Human.csv", nrows=gpt_data.shape[0], usecols=['generated'])

gpt_array = [
    1.0 if float(row.iloc[0].replace('%', 'e-2')) > 1 else float(row.iloc[0].replace('%', 'e-2'))
    for _, row in gpt_data.iterrows()
]
truth_array = [row.iloc[0] for _, row in ground_truth.iterrows()]

difference_array = [
    (truth_array[i] - gpt_array[i]) * 100 for i in range(len(gpt_data))
]
truth = sum(1 for value in truth_array if value == 1)

print(truth)
exit()

values, bins, bars = plt.hist(difference_array, bins=20)
plt.ylabel('Frequency')
plt.xlabel('% Difference')
plt.title("Difference between Ground Truth and ZeroGPT's prediction")
plt.xticks(np.arange(-100, 110, 10))
plt.bar_label(bars, fontsize=10, color='navy')

plt.show()