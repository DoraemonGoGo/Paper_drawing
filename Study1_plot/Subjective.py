import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_name = "likert"
# 假设你的文件名是 "data.xlsx"，请替换为你的实际文件名和路径
file_path = "E:/Desktop/paper/Study1_Data/" + file_name + ".xlsx"

df = pd.read_excel(file_path)

# 计算均值和标准误差，只针对可察觉性、舒适度和感知效果
mean_df = df.groupby(['通知角度', '显示方式'])[['可察觉性', '舒适度', '感知效果']].mean()
sem_df = df.groupby(['通知角度', '显示方式'])[['可察觉性', '舒适度', '感知效果']].sem()  # 标准误差
std_df = df.groupby(['通知角度', '显示方式'])[['可察觉性', '舒适度', '感知效果']].std()  # 计算标准差
# 计算25°和45°整体均值和标准差
mean_25 = mean_df.loc[25].mean()  # 对25°所有显示方式的均值求整体均值
std_25 = std_df.loc[25].mean()  # 对25°所有显示方式的标准差求整体标准差

mean_45 = mean_df.loc[45].mean()  # 对45°所有显示方式的均值求整体均值
std_45 = std_df.loc[45].mean()  # 对45°所有显示方式的标准差求整体标准差

# 输出25°和45°整体均值和标准差
print(f"25°的均值:\n{mean_25}")
print(f"25°的标准差:\n{std_25}")
print(f"\n45°的均值:\n{mean_45}")
print(f"45°的标准差:\n{std_45}")

# 计算每种显示方式下舒适度的均值和标准差
comfortability_stats = df.groupby('显示方式')['舒适度'].agg(['mean', 'std'])

# 输出结果
print(comfortability_stats)

# 创建一个2x3的组合标签
labels = ['25°-Normal', '25°-Blinking', '25°-Vibratory', '45°-Normal', '45°-Blinking', '45°-Vibratory']
x = np.arange(len(labels))

# 条形图的宽度
width = 0.2

# 创建条形图
fig, ax = plt.subplots(figsize=(10, 5))

# 绘制可察觉性条形图
# ax.bar(x - width, mean_df['可察觉性'], width, label='Noticeability', yerr=sem_df['可察觉性'], capsize=5, color='#2DA2FE', alpha=0.7)
ax.bar(x - width, mean_df['可察觉性'], width, label='Noticeability', yerr=sem_df['可察觉性'], capsize=5, color='#1f77b4', alpha=0.9)

# 绘制舒适度条形图
# ax.bar(x, mean_df['舒适度'], width, label='Comfortability', yerr=sem_df['舒适度'], capsize=5, color='#23D96E', alpha=0.7)
ax.bar(x, mean_df['舒适度'], width, label='Comfortability', yerr=sem_df['舒适度'], capsize=5, color='#2ca02c', alpha=0.9)

# 绘制感知效果条形图
# ax.bar(x + width, mean_df['感知效果'], width, label='Perceived effectiveness', yerr=sem_df['感知效果'], capsize=5, color='#FFBA60', alpha=0.7)
ax.bar(x + width, mean_df['感知效果'], width, label='Perceived effectiveness', yerr=sem_df['感知效果'], capsize=5, color='#ff7f0e', alpha=0.9)

# 设置X轴标签
ax.set_xticks(x)
ax.set_xticklabels(labels)
# 调整 x 轴刻度的字体大小
ax.tick_params(axis='x', labelsize=13.5)  # 设置 x 轴刻度标签字体大小为 14
ax.tick_params(axis='y', labelsize=14)  # 设置 x 轴刻度标签字体大小为 14

ax.set_ylim(0, 7)
ax.spines['left'].set_bounds(0, 7)

# 去掉顶部和右侧的边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 显示图例
ax.legend(loc='upper right', fontsize=13, frameon=False)

# 保存为矢量图
plt.savefig("E:/Desktop/paper/Study1_Data/" + file_name + ".jpg", format="jpg", bbox_inches='tight', dpi=300)  # 保存为 SVG 矢量图格式

# 显示图表
plt.tight_layout()
plt.show()
