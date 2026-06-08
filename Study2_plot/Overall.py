import pandas as pd
import matplotlib.pyplot as plt

# plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

# 替换为你的文件路径
file_path = "E:/Desktop/paper/Study2_Data/nasa_tlx_with_total.xlsx"  # 替换为实际的文件路径

# 读取 Excel 文件
df = pd.read_excel(file_path)

# 使用 replace 方法进行条件替换
df['条件'] = df['条件'].replace({'Gaze': 'Graded', 'Icon': 'Icon', 'Head': 'Head-up'})

# 计算每个条件下的总分（即"Overall"列的平均值）
mean_values = df.groupby('条件')['overall'].mean()
se_values = df.groupby('条件')['overall'].sem()  # 使用标准差（SE）作为误差

# 条形图的宽度
bar_width = 0.4
x = range(len(mean_values))

# 条形图的标签和颜色
labels = ['Graded', 'Head-up', 'Icon']
# colors = ['#2DA2FE', '#23D96E', '#FFBA60']
colors = ['#1f77b4', '#2ca02c', '#ff7f0e']

# 绘制条形图
fig, ax = plt.subplots(figsize=(4, 5))

# 循环绘制每个条形图，并设置对应的颜色
for i in range(len(mean_values)):
    ax.bar(
        x[i],
        mean_values.iloc[i],
        bar_width,
        yerr=se_values.iloc[i],  # 使用标准差作为误差线
        capsize=5,  # 设置误差线的端点长度
        color=colors[i],  # 单一颜色值
        alpha=0.9,  # 设置透明度
    )

# 调整Y轴范围，使最低点为 0.5
ax.set_ylim(0, 60)  # 使最大值自动适应数据
ax.set_yticks([0, 10, 20, 30, 40, 50, 60])

# 强制让底部的 Y 轴显示从 0.5 开始，不显示下方
ax.spines['left'].set_bounds(0, 60)
# ax.spines['bottom'].set_bounds(0, 2.2)  # 限制X轴的显示范围从0到2，和X轴刻度相同
ax.set_xticks([0, 1, 2])
# ax.set_xticklabels(['Graded', 'Head-up', 'Icon'], fontsize=13)

# 设置X轴的刻度和标签
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=13)

# 增加 y 轴刻度字体大小
ax.tick_params(axis='y', labelsize=13)

significance_text = '*'
# 显著性比较对及其高度
overall_index = 0
significance_pairs = [(overall_index, overall_index + 1), (overall_index, overall_index + 2)]  # 两个显著性对
pair_heights = [mean_values.max() + 2, mean_values.max() + 5]  # 不同高度

# 添加显著性标记
for (x1, x2), y in zip(significance_pairs, pair_heights):
    h = 0.5  # 间距
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], color='black')
    ax.text((x1 + x2) / 2, y + h, significance_text, ha='center', va='bottom')

# 去掉顶部和右侧的边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 设置标题和Y轴标签
# ax.set_title('NASA TLX', fontsize=14)
# ax.set_xlabel('Condition', fontsize=12)
ax.set_ylabel('Score', fontsize=14)

# 保存为 JPG 文件
plt.savefig("E:/Desktop/paper/Study2_Data/NASA_TLX.jpg", format="jpg", bbox_inches='tight', dpi=300)  # 保存为 JPG 格式

# 调整图表布局并显示
plt.tight_layout()
plt.show()
