import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

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

labels = ['Graded', 'Head-up', 'Icon']
# colors = ['#2DA2FE', '#23D96E', '#FFBA60']
colors = ['#1f77b4', '#2ca02c', '#ff7f0e']

fig, ax = plt.subplots(figsize=(4, 5))

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
ax.spines['left'].set_bounds(0, 60)
ax.set_xticks([0, 1, 2])
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)

significance_text = '*'
overall_index = 0
significance_pairs = [(overall_index, overall_index + 1), (overall_index, overall_index + 2)]  # 两个显著性对
pair_heights = [mean_values.max() + 1, mean_values.max() + 5]  # 不同高度
for (x1, x2), y in zip(significance_pairs, pair_heights):
    h = 0.5  # 间距
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], color='black')
    ax.text((x1 + x2) / 2, y + h, significance_text, ha='center', va='bottom', fontsize=20)


# 去掉顶部和右侧的边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylabel('NASA-TLX 总分', fontsize=20)
# ax.set_xlabel('（a）NASA-TLX 总分', fontsize=20, fontname='Times New Roman')
ax.text(0.45, -0.15, '(a) NASA-TLX 总分', transform=ax.transAxes, ha='center', va='top', fontsize=20, fontweight='normal')

# 保存为 SVG 文件
plt.savefig("E:/Desktop/paper/Study2_Data/NASA_TLX_zh.jpg", format="jpg", bbox_inches='tight', dpi=300)  # 保存为 JPG 格式

# 调整图表布局并显示
plt.tight_layout()
plt.show()
