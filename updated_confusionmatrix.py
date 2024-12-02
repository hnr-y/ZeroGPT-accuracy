from sklearn.metrics import brier_score_loss
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

gpt_data = pd.read_csv("data.csv", usecols=[' zeroGPT Confidence'])
# print(gpt_data.loc[1][' zeroGPT Confidence'])

ground_truth = pd.read_csv("../furtherAIDetectionResearch/AI_Human.csv", nrows=gpt_data.shape[0], usecols=['generated'])
# print(ground_truth.loc[1])
fig, ax = plt.subplots(3, 3, figsize=(50, 50))
# fig.tight_layout()

fig.subplots_adjust(hspace=0.4, wspace=0.4, bottom=0.01, top=0.91)
for x in range(3):
    for y in range(3):
        gpt_array, truth_array = [], []

        threshold = list(range(1, 10))[3 * x + y] / 10
        for _, row in gpt_data.iterrows():
            if float(row.iloc[0].replace('%', 'e-2')) >= threshold:
                gpt_array.append(1.0)
            else:
                gpt_array.append(float(row.iloc[0].replace('%', 'e-2')))
        for _, row in ground_truth.iterrows():
            truth_array.append(row.iloc[0])

        truePositive, trueNegative, falsePositive, falseNegative = 0, 0, 0, 0
        for i in range(len(gpt_array)):
            if gpt_array[i] == 1 and truth_array[i] == 1:
                truePositive += 1
            if gpt_array[i] == 1 and truth_array[i] == 0:
                falsePositive += 1
            if gpt_array[i] == 0 and truth_array[i] == 0:
                trueNegative += 1
            if gpt_array[i] == 0 and truth_array[i] == 1:
                falseNegative += 1
        # print(truePositive, trueNegative, falsePositive, falseNegative)
        print("threshold: " + str(threshold))
        for i in range(1, 11):
            print("assuming " + str(
                i) + " in 10 students use chatGPT, the probability that the student actually used chatGPT given that zeroGPT accuses them of using chatGPT is ",
                  end="")
            print(str((i / 10 * truePositive) / ((i / 10 * truePositive) + (10 - i) / 10 * falsePositive) * 100) + "%")
        print('========================')
        matrix = [[truePositive, falseNegative], [falsePositive, trueNegative]]
        df_cm = pd.DataFrame(matrix, ["GPT generated", "Human Written"], ["GPT generated", "Human Written"])
        # plt.figure(figsize=(10,7))
        sn.set(font_scale=1.4)  # for label size
        plt.xlabel("aaa")
        sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}, ax=ax[x, y], fmt='g')  # font size
        ax[x, y].collections[0].colorbar.ax.tick_params(labelsize=10)
        ax[x, y].tick_params(length=0)
        ax[x, y].xaxis.tick_top()
        ax[x, y].xaxis.set_label_position('top')
        ax[x, y].spines['bottom'].set_visible(False)
        ax[x, y].spines['top'].set_visible(True)
        ax[x, y].set_xlabel("ZeroGPT's prediction")
        ax[x, y].set_ylabel("Ground Truth")
        ax[x, y].set(title="Threshold: " + str(threshold * 100) + "%")
plt.show()
