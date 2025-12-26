import matplotlib.pyplot as plt
import numpy as np

# 设置字体，确保中文可以显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用 SimHei 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题

# 示例数据
angles = [1, 2]  # 角度1 和 角度2
effect_1 = [0.299, 0.254]  # 效果1的估算边际平均值
effect_2 = [0.307, 0.249]  # 效果2的估算边际平均值
effect_3 = [0.328, 0.275]  # 效果3的估算边际平均值

# 标准误差
se_1 = [0.030, 0.030]
se_2 = [0.017, 0.032]
se_3 = [0.032, 0.028]

# 绘制图表
plt.figure(figsize=(8, 6))

# 为了避免重叠，对x轴稍微偏移数据点
offset = 0.05  # 偏移量

# 绘制误差棒图并对 x 轴数据点进行稍微偏移，防止重叠
plt.errorbar([x - offset for x in angles], effect_1, yerr=se_1, fmt='-o', label='效果1', capsize=5, color='blue', linewidth=2, markersize=8)
plt.errorbar(angles, effect_2, yerr=se_2, fmt='-o', label='效果2', capsize=5, color='green', linewidth=2, markersize=8)
plt.errorbar([x + offset for x in angles], effect_3, yerr=se_3, fmt='-o', label='效果3', capsize=5, color='red', linewidth=2, markersize=8)

# 优化标题和标签
plt.title("不同角度和任务效果下的主要任务错误率估算边际平均值", fontsize=16)
plt.xlabel("角度", fontsize=14)
plt.ylabel("主要任务错误率", fontsize=14)

# 优化图例
plt.legend(title="任务效果", loc="upper right", fontsize=12)

# 优化x轴刻度
plt.xticks(angles, ['25', '45'], fontsize=12)
plt.yticks(fontsize=12)

# 添加网格线
plt.grid(True)

# 显示图表
plt.tight_layout()
plt.show()
