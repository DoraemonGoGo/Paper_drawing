import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
from matplotlib.colors import Normalize
import os

plt.rcParams['font.sans-serif'] = ['SimSun']  # 或者 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'stix'


def plot_heatmaps(folder):
    """
    在同一个图中绘制文件夹中所有文件的热力图。

    参数:
    - folder: 文件夹路径
    - lower_threshold: 核密度估计的最小阈值
    - upper_threshold: 核密度估计的最大阈值
    """
    # 获取文件夹中的所有CSV文件
    file_names = [f for f in os.listdir(folder) if f.endswith('.csv')]

    # 检查是否有文件可处理
    if len(file_names) == 0:
        print("文件夹中没有CSV文件。")
        return

    # 限制处理的文件数为6个
    file_names = file_names[:3]

    # 创建绘图画布
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)  # 1行3列的子图
    axes = axes.flatten()  # 将二维数组展平成一维数组以方便遍历

    # 使用 Normalize 来控制颜色条的范围
    lower_threshold = 0.005
    upper_threshold = 0.05
    norm = Normalize(vmin=lower_threshold, vmax=upper_threshold)

    # 遍历每个文件，并绘制对应的热力图
    for i, file_name in enumerate(file_names):
        file_path = os.path.join(folder, file_name)

        # 读取数据
        data = pd.read_csv(file_path)

        # 数据清理
        data = data[data['distance'] <= 1.3]
        data = data[(data['y'] > -2) & (data['y'] < 8)]

        # 获取x和y坐标
        x = data['x']
        y = data['y']

        # 计算x < -0.5 和 y < 0.2 的数据比例
        x_less_than_minus_0_5 = (x < -6).sum() / len(x)  # x < -0.5 的比例
        y_less_than_0_2 = (y < 1.5).sum() / len(y)  # y < 0.2 的比例

        # 打印每个文件的结果
        print(f"文件: {file_name}")
        print(f"x < -0.5 的数据比例: {x_less_than_minus_0_5:.3%}")
        print(f"y < 0.2 的数据比例: {y_less_than_0_2:.3%}\n")

        # 计算核密度估计
        values = np.vstack([x, y])
        kde = gaussian_kde(values)
        density = kde(values)

        # 根据阈值过滤数据
        x_filtered = x[(density >= lower_threshold) & (density <= upper_threshold)]
        y_filtered = y[(density >= lower_threshold) & (density <= upper_threshold)]

        # 绘制热力图
        ax = axes[i]
        sns.kdeplot(x=x_filtered, y=y_filtered, cmap="rocket_r", fill=True, bw_adjust=.5, ax=ax)
        ax.set_title(f'{file_name[:-4]}', fontsize=22)
        ax.set_xlim(-8, 8)
        ax.set_ylim(0, 8)
        # ax.invert_yaxis()  # 反转Y轴

        # 设置刻度字体大小和轴标签字体大小
        ax.tick_params(axis='x', labelsize=22)  # 设置 x 轴刻度字体大小
        ax.tick_params(axis='y', labelsize=22)  # 设置 y 轴刻度字体大小
        ax.set_xlabel('X', fontsize=22)  # 设置 x 轴标签和字体大小
        ax.set_ylabel('Y', fontsize=22)  # 设置 y 轴标签和字体大小

        # 在每个子图上添加x=-4和y=2的蓝色虚线
        # ax.axvline(x=-5, color='#2DA2FE', linestyle='--', label='x = -4')  # 垂直虚线
        # ax.axhline(y=2, color='#2DA2FE', linestyle='--', label='y = 2')    # 水平虚线

        # 获取当前的刻度，并将它们缩小10倍
        x_ticks = ax.get_xticks()  # 获取当前x轴刻度
        y_ticks = ax.get_yticks()  # 获取当前y轴刻度

        # 设置新的刻度位置和标签，将刻度缩小10倍
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_ticks / 10)  # 将x轴刻度标签缩小10倍
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_ticks / 10)  # 将y轴刻度标签缩小10倍

    # 隐藏未使用的子图
    for j in range(len(file_names), 3):
        fig.delaxes(axes[j])

    # 添加整体的颜色条
    sm = plt.cm.ScalarMappable(cmap="rocket_r", norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=axes, orientation='vertical', fraction=0.02, pad=0.04)
    cbar.set_label('密度', fontsize=22)
    cbar.ax.tick_params(labelsize=22)  # 控制颜色条刻度字体大小

    # 设置整体图表的标题
    # plt.suptitle('Heatmaps of Eye Gaze Data(Heavy Task)', fontsize=18)
    # plt.tight_layout(rect=[0, 0, 1, 0.96])  # 调整布局
    fig.supxlabel('(b) 重负荷', fontsize=26)

    # 保存为矢量图
    plt.savefig("E:/Desktop/paper/Study2_Data/merged_files/heatmap_high.png", format="png",
                bbox_inches='tight', dpi=300)  # 保存为 PNG 图片格式

    # 显示图表
    plt.show()

# 示例用法
folder = 'E:/Desktop/paper/Study2_Data/merged_files/HighTask'  # 替换为实际的文件夹路径
plot_heatmaps(folder)
