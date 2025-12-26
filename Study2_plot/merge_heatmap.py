import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
from matplotlib.colors import Normalize
import os

def plot_low_and_high(low_folder, high_folder):
    # 取各自文件列表（最多3个）
    low_files  = [f for f in os.listdir(low_folder)  if f.endswith('.csv')][:3]
    high_files = [f for f in os.listdir(high_folder) if f.endswith('.csv')][:3]

    # 统一阈值和颜色映射
    lower_threshold = 0.005
    upper_threshold = 0.05
    norm = Normalize(vmin=lower_threshold, vmax=upper_threshold)

    # 一次性创建 2行×3列，公用 x/y 轴
    fig, axes = plt.subplots(
        nrows=2, ncols=3,
        figsize=(18, 12),
        sharex=True, sharey=True,
        constrained_layout=True
    )

    # 内部画图函数，给定轴和文件路径
    def draw_kde(ax, file_path, title):
        data = pd.read_csv(file_path)
        data = data[data['distance'] <= 1.3]
        data = data[(data['y'] > -2) & (data['y'] < 8)]
        x, y = data['x'], data['y']

        # 核密度
        values  = np.vstack([x, y])
        density = gaussian_kde(values)(values)
        mask    = (density >= lower_threshold) & (density <= upper_threshold)
        sns.kdeplot(x=x[mask], y=y[mask],
                    cmap="Reds", fill=True, bw_adjust=0.5, ax=ax)

        ax.set_title(title, fontsize=26)
        ax.set_xlim(-8, 8)
        ax.set_ylim(0, 8)
        ax.set_xlabel('X', fontsize=24)
        ax.set_ylabel('Y', fontsize=24)
        ax.tick_params(labelsize=24)

    # 第一行：LowTask
    for col, fname in enumerate(low_files):
        ax = axes[0, col]
        draw_kde(ax, os.path.join(low_folder, fname), title=f"Low – {fname[:-4]}")

    # 第二行：HighTask
    for col, fname in enumerate(high_files):
        ax = axes[1, col]
        draw_kde(ax, os.path.join(high_folder, fname), title=f"High – {fname[:-4]}")

    # 整体 colorbar
    sm = plt.cm.ScalarMappable(cmap="Reds", norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(
        sm, ax=axes.ravel().tolist(),
        orientation='vertical', fraction=0.02, pad=0.04
    )
    cbar.set_label('Density', fontsize=26)
    cbar.ax.tick_params(labelsize=24)

    plt.savefig(r"E:/Desktop/Study2_Data/merged_files/heatmap_comparison.jpg",
                dpi=300, bbox_inches='tight')

    plt.show()


# 调用示例
plot_low_and_high(
    'E:/Desktop/Study2_Data/merged_files/LowTask',
    'E:/Desktop/Study2_Data/merged_files/HighTask'
)
