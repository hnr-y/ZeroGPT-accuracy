from sklearn.metrics import brier_score_loss
import pandas as pd

gpt_data = pd.read_csv("data.csv", usecols=[' zeroGPT Confidence'])
ground_truth = pd.read_csv("../furtherAIDetectionResearch/AI_Human.csv", nrows=gpt_data.shape[0], usecols=['generated'])

gpt_array = [
    1.0 if float(row.iloc[0].replace('%', 'e-2')) > 1 else float(row.iloc[0].replace('%', 'e-2'))
    for _, row in gpt_data.iterrows()
]
truth_array = [row.iloc[0] for _, row in ground_truth.iterrows()]

brier_score = brier_score_loss(truth_array, gpt_array)
print(brier_score)