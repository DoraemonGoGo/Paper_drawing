import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
from matplotlib.colors import Normalize

# 读取CSV文件
data = pd.read_csv('E:/Desktop/paper/Study2_Data/merged_files/merged_eye_tracking_data_HighTask_cameraTrack.csv')

# 删除第四列中大于1的行
data = data[data['distance'] <= 1]
data = data[data['y'] <= 8.5]
# 保存处理后的数据到CSV文件
# data.to_csv('E:/Desktop/Study2_Data/filtered_Blink.csv', index=False)

# 获取x和y坐标
x = data['x']
y = data['y']

# 使用scipy的gaussian_kde计算核密度估计
values = np.vstack([x, y])
kde = gaussian_kde(values)
density = kde(values)

# 设置核密度阈值
lower_threshold = 0.007
upper_threshold = 0.055
x_filtered = x[(density >= lower_threshold) & (density <= upper_threshold)]
y_filtered = y[(density >= lower_threshold) & (density <= upper_threshold)]

# 绘制过滤后的热力图
plt.figure(figsize=(10, 8))
ax = sns.kdeplot(x=x_filtered, y=y_filtered, cmap="Reds", fill=True, bw_adjust=.5, cbar=True)

# 设置x轴的范围为[-8, 8]
plt.xlim(-8, 8)
plt.ylim(0, 11)

# 设置图表标题和标签
plt.title('Filtered Heatmap of Eye Gaze Data (KDE Threshold)')
plt.xlabel('X Position')
plt.ylabel('Y Position')

plt.gca().invert_yaxis()  # 反转Y轴
plt.show()
