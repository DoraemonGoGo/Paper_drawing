import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def create_stacked_bar_chart_from_excel(excel_file):
    # 从Excel文件中读取数据
    df = pd.read_excel(excel_file)

    # 将列名重命名为英文
    df.rename(columns={
        '25+震动': '25°-Vibratory',
        '25+闪烁': '25°-Blinking',
        '25+正常': '25°-Normal',
        '45+震动': '45°-Vibratory',
        '45+闪烁': '45°-Blinking',
        '45+正常': '45°-Normal'
    }, inplace=True)

    # 定义组合列
    combinations = ['25°-Normal', '25°-Blinking', '25°-Vibratory', '45°-Normal', '45°-Blinking', '45°-Vibratory']

    # 计算每个组合的平均评分
    average_scores = df[combinations].mean()

    # 统计每个组合的评分分布（1-6）
    rating_distribution = np.zeros((6, 6))  # 6个组合，6个评分类别
    for i, col in enumerate(combinations):
        # 获取每个组合的评分分布
        counts = pd.Series(df[col]).value_counts().sort_index()
        for score in range(1, 7):  # 确保处理每个评分1-6
            if score in counts:
                rating_distribution[i, score - 1] = counts[score]  # 存储每个评分的计数

    # 转换成比例
    rating_proportions = rating_distribution / 12

    # 反转 rating_proportions 以匹配标签的顺序
    rating_proportions = rating_proportions[::-1]
    average_scores = average_scores[::-1]
    # 创建堆叠条形图
    fig, ax = plt.subplots(figsize=(10, 5))

    # 初始化堆叠底部，平均评分决定条形的**位置**
    for i, avg in enumerate(average_scores):
        bottom = avg - rating_proportions[i].sum() / 2 # 保证条形围绕平均值分布

        # 定义颜色
        colors = ['#d9ead3', '#b6d7a8', '#93c47d', '#6aa84f', '#38761d', '#274e13']

        # 绘制每个组合的条形图，包含6个不同颜色
        for j in range(6):
            ax.barh(i, rating_proportions[i, j], left=bottom, color=colors[j], label=f'{j+1}' if i == 0 else "")
            bottom += rating_proportions[i, j]  # 逐步堆叠

    # 设置标签和轴
    ax.set_yticks(np.arange(len(combinations)))
    ax.set_yticklabels(combinations[::-1], fontsize=14)
    # ax.set_xlabel(fontsize=12)
    ax.set_xlim(1, 6.2)  # 确保x轴范围从0到6
    # ax.set_title('Preference', fontsize=14)
    # 调整 x 轴刻度的字体大小
    ax.tick_params(axis='x', labelsize=14)  # 设置 x 轴刻度标签字体大小为 14
    # 移除所有的边框
    for spine in ax.spines.values():
        spine.set_visible(False)

    # 移除y轴的刻度线
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')
    # 移除网格线
    ax.grid(False)

    # 添加网格和图例
    plt.grid(True, axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.legend(loc='lower center', frameon=False, bbox_to_anchor=(0.5, -0.19), ncol=6, fontsize=13)

    # 调整布局和底部边距
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.14)  # 增加图形底部边距

    # 保存为矢量图
    plt.savefig("E:/Desktop/Study1_Data/Preference.jpg", format="jpg", bbox_inches='tight', dpi=300)  # 保存为 SVG 矢量图格式

    plt.show()

# 使用方法
create_stacked_bar_chart_from_excel('E:/Desktop/Study1_Data/preference.xlsx')
