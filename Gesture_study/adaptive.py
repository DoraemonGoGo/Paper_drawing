import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# ==========================================
# 1. 全局设置
# ==========================================
# 设置中文字体 (Windows用SimHei，Mac用Arial Unicode MS)
plt.rcParams['font.sans-serif'] = ['SimSun'] 
plt.rcParams['axes.unicode_minus'] = False 

# 设置统一的配色方案 (学术蓝 vs 活力橙)
colors = ["#4c72b0", "#dd8452"]
sns.set_style("whitegrid", {"font.sans-serif": ['SimSun']})

# ==========================================
# 2. 数据准备 (最新数据)
# ==========================================
data_dict = {
    "Sitting_Leg": {
        "Baseline": [92.2, 90, 91.1, 90, 90, 88.9, 94.4, 92.2, 91.1, 90],
        "Adaptive": [96.7, 94.4, 95.6, 95.6, 93.3, 94.4, 97.8, 96.7, 95.6, 95.6]
    },
    "Standing_Leg": {
        "Baseline": [91.1, 90, 88.9, 87.8, 90, 87.8, 91.1, 90, 90, 88.9],
        "Adaptive": [92.2, 92.2, 91.1, 93.3, 92.2, 93.3, 93.3, 94.4, 93.3, 91.1]
    },
    "Hand_Back": {
        "Baseline": [91.1, 91.1, 88.9, 91.1, 90, 87.8, 91.1, 92.2, 87.8, 90],
        "Adaptive": [94.4, 95.6, 92.2, 93.3, 93.3, 92.2, 95.6, 94.4, 92.2, 93.3]
    },
    "Air_Gesture": {
        "Baseline": [90, 87.8, 86.7, 85.6, 87.8, 85.6, 87.8, 87.8, 88.9, 86.7],
        "Adaptive": [92.2, 90, 88.9, 88.9, 91.1, 90, 91.1, 91.1, 91.1, 90]
    }
}

# 数据转换
records = []
labels_map = {
    "Sitting_Leg": "坐姿腿部", 
    "Standing_Leg": "站姿腿部", 
    "Hand_Back": "手背平面", 
    "Air_Gesture": "空中手势"
}

for cond, modes in data_dict.items():
    for mode_name, values in modes.items():
        for v in values:
            records.append({"Condition": labels_map[cond], "Accuracy": v, "Method": mode_name})

df = pd.DataFrame(records)

# ==========================================
# 3. 绘制并保存图 1：条形图 (Bar Chart)
# ==========================================
plt.figure(figsize=(8, 6)) # 单图尺寸
sns.barplot(x="Condition", y="Accuracy", hue="Method", data=df,
                  palette=colors, capsize=.1, errorbar=('ci', 95), errwidth=1.5)

# 添加数值标签
# for p in ax1.patches:
#     if p.get_height() > 0:
#         ax1.annotate(f'{p.get_height():.1f}', 
#                      (p.get_x() + p.get_width() / 2., p.get_height()), 
#                      ha='center', va='center', xytext=(0, 8), 
#                      textcoords='offset points', fontsize=10, fontweight='bold')

# 设置图 1 细节
plt.ylim(84, 100)
plt.tick_params(labelsize=16)
plt.ylabel("平均识别准确率 (%)", fontsize=16)
plt.xlabel("", fontsize=16)
# plt.title("自适应校准前后平均准确率对比", fontsize=14, pad=15)
plt.legend(loc='upper right', frameon=True, fontsize=16)

# 保存图 1
plt.tight_layout()
plt.savefig('Figure_1_BarChart.png', dpi=300)
print("图 1 已生成: Figure_1_BarChart.png")
plt.clf() # 清空画布，准备画下一张

# ==========================================
# 4. 绘制并保存图 2：箱线图 (Box Plot)
# ==========================================
plt.figure(figsize=(8, 6)) # 单图尺寸

# 绘制箱线图
ax = sns.boxplot(x="Condition", y="Accuracy", hue="Method", data=df,
            palette=colors, width=0.5, linewidth=1.5, fliersize=0)

# 叠加散点图
sns.swarmplot(x="Condition", y="Accuracy", hue="Method", data=df,
              dodge=True, size=5, color=".2", alpha=0.7)

# 设置图 2 细节
plt.ylim(84, 100) # 保持和图1一致的Y轴范围
plt.tick_params(labelsize=16)
plt.ylabel("准确率分布 (%)", fontsize=16)
plt.xlabel("", fontsize=16)
# plt.title("准确率分布与个体差异分析", fontsize=14, pad=15)
handles, labels = ax.get_legend_handles_labels()
plt.legend(handles[0:2], ["Baseline", "Adaptive"], 
           loc='upper right', frameon=True, fontsize=16)

# 保存图 2
plt.tight_layout()
plt.savefig('Figure_2_BoxPlot.png', dpi=300)
print("图 2 已生成: Figure_2_BoxPlot.png")
plt.show()