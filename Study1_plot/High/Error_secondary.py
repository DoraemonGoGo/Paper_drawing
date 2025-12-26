import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats  # 用于计算标准误差

file_name = "次要任务错误次数High"
# 假设你的文件名是 "data.xlsx"，请替换为你的实际文件名和路径
file_path = "E:/Desktop/Study1_Data/High Task/" + file_name + ".xlsx"

# 读取Excel文件
df = pd.read_excel(file_path)

# 将每个次要任务反应时间的数据除以 10
df['次要任务错误次数'] = df['次要任务错误次数'] / 10

# 计算均值和标准误差
mean_df = df.groupby(['角度', '效果'])['次要任务错误次数'].mean().unstack()
std_df = df.groupby(['角度', '效果'])['次要任务错误次数'].apply(stats.sem).unstack()
std_df2 = df.groupby(['角度', '效果'])['次要任务错误次数'].std().unstack()  # 计算标准差

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
ax.errorbar(x_shifted_left, mean_df.loc[25], yerr=std_df.loc[25], fmt='o-', capsize=4, label='25', color='#2DA2FE')

# 绘制45度角数据
ax.errorbar(x_shifted_right, mean_df.loc[45], yerr=std_df.loc[45], fmt='o-', capsize=4, label='45', color='#23D96E')

# 调整Y轴范围，使最低点为 0.5
ax.set_ylim(-0.005, 0.1)  # 使最大值自动适应数据
ax.set_xlim(-0.3, 2.5)
# 调整 x 轴刻度的字体大小
ax.tick_params(axis='x', labelsize=12)  # 设置 x 轴刻度标签字体大小为 14
ax.tick_params(axis='y', labelsize=12)  # 设置 x 轴刻度标签字体大小为 14
ax.set_yticks([0, 0.02, 0.04, 0.06, 0.08, 0.1])

# 强制让底部的 Y 轴显示从 0.5 开始，不显示下方
ax.spines['left'].set_bounds(0, 0.1)

# 强制让底部的 X 轴只显示三个点之间的范围
ax.spines['bottom'].set_bounds(0, 2)  # 限制X轴的显示范围从0到2，和X轴刻度相同

# 强制将 X 轴设置在 Y 轴的 0.3 位置
ax.spines['bottom'].set_position(('data', -0.01))  # 让X轴位于Y轴的0.3位置

# 设置X轴的刻度和标签
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Normal', 'Blinking', 'Vibratory'])

# 去掉顶部和右侧的边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 设置标题和Y轴标签
ax.set_title('ER(Secondary Task,Heavy)', fontsize=12)
ax.set_ylabel('Error Rate', fontsize=12)
# ax.set_ylim(0, max(mean_df.max()) + 1)  # 调整Y轴范围

# 显示图例
ax.legend(loc='upper right', fontsize=12, frameon=False)

# 保存为矢量图
plt.savefig("E:/Desktop/Study1_Data/High Task/" + file_name + ".jpg", format="jpg", bbox_inches='tight', dpi=300)  # 保存为 SVG 矢量图格式

# 显示图表
plt.tight_layout()
plt.show()
