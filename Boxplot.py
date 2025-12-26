import matplotlib.pyplot as plt
import numpy as np

# 生成示例数据
np.random.seed(42)
circular_data = [np.random.normal(98, 1, 100), np.random.normal(5, 1, 100), np.random.normal(4, 1, 100), np.random.normal(3, 1, 100)]
linear_data = [np.random.normal(96, 2, 100), np.random.normal(6, 1.5, 100), np.random.normal(5, 1.5, 100), np.random.normal(4, 1.5, 100)]
text_data = [np.random.normal(92, 4, 100), np.random.normal(7, 2, 100), np.random.normal(6, 2, 100), np.random.normal(5, 2, 100)]

# 创建子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# 1. Progress Perception
ax1.boxplot([circular_data[0], linear_data[0], text_data[0]],
            patch_artist=True,
            showmeans=True)

# 自定义颜色
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
for patch, color in zip(ax1.artists, colors):
    patch.set_facecolor(color)

# 设置X轴标签
ax1.set_xticklabels(['Circular', 'Linear', 'Text'])
ax1.set_title('(a) Progress perception')
ax1.set_ylabel('Progress Accuracy %')

# 2. Quality of Conversation
ax2.boxplot([circular_data[1], linear_data[1], text_data[1]],
            patch_artist=True,
            showmeans=True)

# 自定义颜色
for patch, color in zip(ax2.artists, colors):
    patch.set_facecolor(color)

# 设置X轴标签
ax2.set_xticklabels(['Circular', 'Linear', 'Text'])
ax2.set_title('(b) Quality of conversation')
ax2.set_ylabel('Degree of Distraction %')

# 添加图表标题和其他配置
plt.suptitle('Comparison of Circular, Linear, and Text Notifications', fontsize=16)

# 显示图表
plt.show()
