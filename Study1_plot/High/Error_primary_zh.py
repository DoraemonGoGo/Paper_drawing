import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats  # 用于计算标准误差

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

file_name = "主错误率High"
# 假设你的文件名是 "data.xlsx"，请替换为你的实际文件名和路径
file_path = "E:/Desktop/paper/Study1_Data/High Task/" + file_name + ".xlsx"

# 读取Excel文件
df = pd.read_excel(file_path)

# 计算均值和标准误差
mean_df = df.groupby(['角度', '效果'])['主要任务错误率'].mean().unstack()
std_df = df.groupby(['角度', '效果'])['主要任务错误率'].apply(stats.sem).unstack()
std_df2 = df.groupby(['角度', '效果'])['主要任务错误率'].std().unstack()  # 计算标准差

# 输出标准差
print("标准差：")
print(std_df2)

# 创建一个图
fig, ax = plt.subplots(figsize=(4, 5))

# 使用 mean_df 的列标签作为 X 轴的标签
x = mean_df.columns

# 给每组数据的 X 轴位置增加一点偏移，使其错开
x_shifted_left = [i - 0.05 for i in range(len(x))]  # 左移一组
x_shifted_right = [i + 0.05 for i in range(len(x))]  # 右移一组

# 绘制25度角数据
# ax.errorbar(x_shifted_left, mean_df.loc[25], yerr=std_df.loc[25], fmt='o-', capsize=4, label='25°', color='#2DA2FE')
ax.errorbar(x_shifted_left, mean_df.loc[25], yerr=std_df.loc[25], fmt='o-', capsize=4, label='25°', color='#1f77b4')

# 绘制45度角数据
# ax.errorbar(x_shifted_right, mean_df.loc[45], yerr=std_df.loc[45], fmt='o-', capsize=4, label='45°', color='#23D96E')
ax.errorbar(x_shifted_right, mean_df.loc[45], yerr=std_df.loc[45], fmt='s-', capsize=4, label='45°', color='#ff7f0e')

# 调整Y轴范围，使最低点为 0.5
ax.set_ylim(0.2, 0.45)  # 使最大值自动适应数据
ax.set_xlim(-0.3, 2.5)
# 调整 x 轴刻度的字体大小
ax.tick_params(axis='x', labelsize=16)  # 设置 x 轴刻度标签字体大小为 14
ax.tick_params(axis='y', labelsize=16)  # 设置 x 轴刻度标签字体大小为 14
# ax.set_yticks([0.2, 0.3, 0.4, 0.5, 0.6])

ax.spines['left'].set_bounds(0.2, 0.45)

# 强制让底部的 X 轴只显示三个点之间的范围
ax.spines['bottom'].set_bounds(0, 2)  # 限制X轴的显示范围从0到2，和X轴刻度相同

# 强制将 X 轴设置在 Y 轴的 0.3 位置
ax.spines['bottom'].set_position(('data', 0.1875))  # 让X轴位于Y轴的0.3位置

# 设置X轴的刻度和标签
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['正常', '闪烁', '震动'])

# 去掉顶部和右侧的边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)


# 设置标题和Y轴标签
# ax.set_title('主要任务错误率 (重负荷)', fontsize=16, fontweight='bold')
ax.set_ylabel('错误率', fontsize=16, fontweight='bold')
ax.text(0.4, -0.2, '(b) 错误率 (重负荷)', transform=ax.transAxes, ha='center', va='top', fontsize=17, fontweight='normal')
# ax.set_ylim(0, max(mean_df.max()) + 1)  # 调整Y轴范围

# 显示图例
legend = ax.legend(loc='upper right', prop={'weight': 'bold', 'size': 16}, frameon=False, bbox_to_anchor=(1, 1))
# 保存为矢量图
plt.savefig("E:/Desktop/paper/Study1_Data/High Task/" + file_name + "_zh.jpg", format="jpg", bbox_inches='tight', dpi=300)  # 保存为 PDF 矢量图格式

# 显示图表
plt.tight_layout()
plt.show()
