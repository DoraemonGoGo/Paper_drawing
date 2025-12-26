import pandas as pd
import matplotlib.pyplot as plt

# 替换为你的文件路径
file_path = "E:/Desktop/Study2_Data/NASA_TLX.xlsx"  # 替换为实际的文件路径

# 读取 Excel 文件
df = pd.read_excel(file_path)
df2 = df
# 计算每个实验人员在每个条件下的总分（所有指标的平均值），排除“实验人员”和“条件”列
df2['overall'] = df2.iloc[:, 2:].mean(axis=1)

# 将数据保存回 Excel 文件，添加总分列
output_file_path = "E:/Desktop/Study2_Data/nasa_tlx_with_total.xlsx"  # 保存新文件的路径
df2.to_excel(output_file_path, index=False)

# 计算每个条件下各个指标的平均值
mean_values = df.groupby('条件').mean().drop(columns=['实验人员'])

# 计算标准误差
sem_values = df.groupby('条件').sem().drop(columns=['实验人员'])

# 去掉 "overall" 列
mean_values = mean_values.drop(columns=['overall'])
sem_values = sem_values.drop(columns=['overall'])

# 绘制条形图
fig, ax = plt.subplots(figsize=(14, 7))

# 获取条件名称
conditions = mean_values.index
# 获取指标名称（包括总分）
metrics = mean_values.columns

# 条形图的宽度
bar_width = 0.2
# 条形图的X轴位置
x = range(len(metrics))

# 设置新的图例标签
legend_labels = ['Graded', 'Head-up', 'Icon']
colors = ['#2DA2FE', '#23D96E', '#FFBA60']

# 遍历每个条件，绘制对应的条形图
for i, condition in enumerate(conditions):
    ax.bar(
        [pos + i * bar_width for pos in x],
        mean_values.loc[condition],
        bar_width,
        label=legend_labels[i],
        yerr=sem_values.loc[condition],  # 添加误差线
        capsize=5,  # 设置误差线的长度
        color = colors[i],  # 单一颜色值
        alpha = 0.7  # 设置透明度
    )

# 设置X轴的刻度和标签
ax.set_xticks([pos + bar_width for pos in x])
ax.set_xticklabels(['Mental Demand', 'Physical\nDemand', 'Temporal\nDemand', 'Performance\nDemand', 'Effort', 'Frustration'], fontsize=15)
# ax.set_xticklabels(metrics, fontsize=13)

# 调整Y轴刻度字体大小
ax.tick_params(axis='y', labelsize=15)  # 设置Y轴刻度字体大小

ax.set_ylim(0, 70)
ax.spines['left'].set_bounds(0, 70)

# 去掉顶部和右侧的边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 显示图例
ax.legend(loc='upper left', fontsize=15, frameon=False, ncol=3)

# 调整图表布局并显示
plt.tight_layout()

# 保存为矢量图
plt.savefig("E:/Desktop/Study2_Data/nasa_tlx_with_total.jpg", format="jpg", dpi=300)  # 保存为 SVG 矢量图格式

plt.show()
