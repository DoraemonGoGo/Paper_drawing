import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False

# 读取CSV文件
file_path = 'E:/Desktop/paper/Study2_Data/Recall.xlsx'  # 请替换为实际文件名
df = pd.read_excel(file_path)

# 计算每种条件和负荷下的平均Recall、标准差(SD)和标准误差(SE)
average_recall = df.groupby(['条件', '负荷'])['Recall'].agg(['mean', 'std', 'sem']).reset_index()

print("条件与负荷组合的平均值和标准差：")
for index, row in average_recall.iterrows():
    print(f"条件: {row['条件']}, 负荷: {row['负荷']}, 平均值: {row['mean']:.4f}, 标准差: {row['std']:.4f}")

# 计算Heavy和Light负荷的平均值和标准差
heavy_light_recall = df[df['条件'].isin(['Gaze', 'Head', 'Icon'])]  # 只选择Heavy和Light负荷
heavy_light_recall = heavy_light_recall.groupby(['条件'])['Recall'].agg(['mean', 'std']).reset_index()

print("\nHeavy和Light负荷下的平均值和标准差：")
for index, row in heavy_light_recall.iterrows():
    print(f"条件: {row['条件']}, 平均值: {row['mean']:.4f}, 标准差: {row['std']:.4f}")

# 创建一个图
fig, ax = plt.subplots(figsize=(4, 5))

# 设置x轴的偏移量
offset = 0.1
conditions = np.arange(len(average_recall['条件'].unique()))

# 自定义颜色
# colors = {'Heavy': '#2DA2FE', 'Light': '#23D96E'}
colors = {'Heavy': '#1f77b4', 'Light': '#ff7f0e'}
markers = {'Heavy': 'o', 'Light': 's'}
label_map = {'Heavy': '重负荷', 'Light': '轻负荷'}

# 为Heavy和Light的平均Recall绘制两条折线，并添加误差线
for i, load in enumerate(['Heavy', 'Light']):
    subset = average_recall[average_recall['负荷'] == load]
    # 计算偏移后的x轴位置
    x_positions = conditions + (i - 0.5) * offset
    # plt.errorbar(x_positions, subset['mean'], yerr=subset['sem'], marker='o', label=label_map[load], capsize=5, color=colors[load])
    plt.errorbar(x_positions, subset['mean'], yerr=subset['sem'], marker=markers[load], label=label_map[load], capsize=5, color=colors[load])

# 调整Y轴范围，使最低点为 0.5
ax.set_ylim(4, 6)  # 使最大值自动适应数据
ax.set_xlim(-0.3, 2.2)
# 调整 x 轴刻度的字体大小
ax.tick_params(axis='x', labelsize=16)  # 设置 x 轴刻度标签字体大小为 22
ax.tick_params(axis='y', labelsize=16)  # 设置 x 轴刻度标签字体大小为 22

ax.set_yticks([4, 4.5, 5, 5.5, 6])

# 强制让底部的 Y 轴显示从 0.5 开始，不显示下方
ax.spines['left'].set_bounds(4, 6)

# 强制让底部的 X 轴只显示三个点之间的范围
ax.spines['bottom'].set_bounds(0, 2)  # 限制X轴的显示范围从0到2，和X轴刻度相同

# 强制将 X 轴设置在 Y 轴的 0.3 位置
ax.spines['bottom'].set_position(('data', 3.875))  # 让X轴位于Y轴的0.3位置

# 添加标题和标签
plt.ylabel('回忆准确率', fontsize=16, fontweight='bold')
# ax.text(0.4, -0.15, '(c)', transform=ax.transAxes, ha='center', va='top', fontsize=18, fontweight='normal', fontname='Times New Roman')
ax.text(0.45, -0.2, '(c) 回忆准确率', transform=ax.transAxes, ha='center', va='top', fontsize=17, fontweight='normal')

# 设置X轴的刻度和标签
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Graded', 'Head-up', 'Icon'], fontsize=16)

# 去掉顶部和右侧的边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 设置图例，去掉框线
# ax.legend(loc='upper right', frameon=False, fontsize=16)
ax.legend(loc='upper right', bbox_to_anchor=(1.04, 1), frameon=False, fontsize=16)

# 保存为矢量图
plt.savefig("E:/Desktop/paper/Study2_Data/Recall_zh.jpg", format="jpg", bbox_inches='tight', dpi=300)  # 保存为 JPG 格式

# 显示图表
plt.grid(False)
# 调整布局，确保边距足够显示
plt.tight_layout()
plt.show()
