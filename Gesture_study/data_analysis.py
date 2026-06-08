import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# from statsmodels.stats.anova import AnovaRM

# =================配置区域=================
INPUT_FILE = 'E:\\Desktop\\gesture_study\\static_data.csv'
OUTPUT_PLOT_1 = 'Experiment_Results_Plot_1.png'  # 主任务图
OUTPUT_PLOT_2 = 'Experiment_Results_Plot_2.png'  # 操作时间图
OUTPUT_REPORT = 'Experiment_Analysis_Report.txt'
FONT_FAMILY = ['SimSun'] # Win用户通常用SimHei，Mac用户可能需要改用Arial Unicode MS
# =========================================

# 1. 读取数据
try:
    df = pd.read_csv(INPUT_FILE)
    df['负荷'] = df['负荷'].map({'轻': '轻负荷', '重': '重负荷'})
except FileNotFoundError:
    print(f"错误：找不到文件 {INPUT_FILE}")
    exit()

# 2. 设置绘图风格
sns.set_context("paper", font_scale=1.4)
sns.set_style("ticks") # 简洁风格
plt.rcParams['font.sans-serif'] = FONT_FAMILY
plt.rcParams['axes.unicode_minus'] = False

# 2.5 计算描述性统计（均值和标准差）
print("\n" + "="*60)
print("描述性统计分析：均值和标准差")
print("="*60 + "\n")

# 所有指标列
all_metrics = ['主任务反应时间', '主任务错误率', '一阶段操作时间', '二阶段操作时间']

# 按类型和负荷分组计算均值和标准差
desc_stats = df.groupby(['类型', '负荷'])[all_metrics].agg(['mean', 'std'])
print("按交互类型和认知负荷分组的统计数据：")
print(desc_stats)
print("\n")

# 保存描述性统计到CSV文件
desc_stats.to_csv('Experiment_Stats.csv', encoding='utf-8-sig')
print("描述性统计已保存为: Experiment_Stats.csv\n")

# 3. 定义绘图顺序和标签 (按要求排序)
metrics_config_1 = [
    # (列名, Y轴标签, 图表标题)
    ('主任务反应时间', '反应时间 (s)', '（a）主要任务反应时间'),
    ('主任务错误率', '错误率', '（b）主要任务错误率'),
]

metrics_config_2 = [
    ('一阶段操作时间', '操作时间 (s)', '（a）通知感知时间'),
    ('二阶段操作时间', '操作时间 (s)', '（b）快捷回复时间')
]

# 4. 绘制第一张图：主任务指标
fig1, axes1 = plt.subplots(1, 2, figsize=(14, 5.5))

for i, (col, ylabel, title) in enumerate(metrics_config_1):
    ax = axes1[i]
    
    # 绘制柱状图
    sns.barplot(
        x='负荷', y=col, hue='类型', data=df, 
        ax=ax,
        palette=['#4c72b0', '#c44e52'],
        capsize=.1, 
        errorbar=('ci', 95),
        edgecolor=".3",
        linewidth=1.5
    )
    
    # 设置标题和标签
    # ax.set_title(title, fontweight='bold', fontsize=16, pad=10) # 移除顶部标题
    ax.text(0.5, -0.1, title, transform=ax.transAxes, 
            ha='center', va='top', fontsize=18) # 移动到底部
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_xlabel("", fontsize=16, labelpad=8)
    
    # 设置刻度标签大小
    ax.tick_params(axis='both', labelsize=16)
    
    # 移除子图自带的图例
    if ax.get_legend():
        ax.get_legend().remove()
    
    # 美化边框
    sns.despine(ax=ax)

# 添加统一图例
handles, labels = axes1[0].get_legend_handles_labels()
fig1.legend(handles, labels, loc='upper right', bbox_to_anchor=(0.92, 0.92), 
           title='交互方式', fontsize=14, title_fontsize=14, 
           frameon=True, edgecolor='.8')

plt.tight_layout()
plt.subplots_adjust(bottom=0.2, right=0.88, top=0.92)
plt.savefig(OUTPUT_PLOT_1, dpi=300, bbox_inches='tight')
print(f"图表1已保存为: {OUTPUT_PLOT_1}")
plt.close()

# 5. 绘制第二张图：操作时间指标
fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5.5))

for i, (col, ylabel, title) in enumerate(metrics_config_2):
    ax = axes2[i]
    
    # 绘制柱状图
    sns.barplot(
        x='负荷', y=col, hue='类型', data=df, 
        ax=ax,
        palette=['#4c72b0', '#c44e52'],
        capsize=.1, 
        errorbar=('ci', 95),
        edgecolor=".3",
        linewidth=1.5
    )
    
    # 设置标题和标签
    # ax.set_title(title, fontweight='bold', fontsize=16, pad=10) # 移除顶部标题
    ax.text(0.5, -0.1, title, transform=ax.transAxes, 
            ha='center', va='top', fontsize=18) # 移动到底部
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_xlabel("", fontsize=16, labelpad=8)
    
    # 设置刻度标签大小
    ax.tick_params(axis='both', labelsize=16)
    
    # 移除子图自带的图例
    if ax.get_legend():
        ax.get_legend().remove()
    
    # 美化边框
    sns.despine(ax=ax)

# 添加统一图例
handles, labels = axes2[0].get_legend_handles_labels()
fig2.legend(handles, labels, loc='upper right', bbox_to_anchor=(0.92, 0.92), 
           title='交互方式', fontsize=13, title_fontsize=13, 
           frameon=True, edgecolor='.8')

plt.tight_layout()
plt.subplots_adjust(bottom=0.2, right=0.88, top=0.92)
plt.savefig(OUTPUT_PLOT_2, dpi=300, bbox_inches='tight')
print(f"图表2已保存为: {OUTPUT_PLOT_2}")

# # 7. 导出统计分析报告
# with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
#     f.write("实验数据统计分析报告\n")
#     f.write("========================================\n\n")
    
#     for col, _, title in metrics_config:
#         f.write(f"指标分析: {title}\n")
#         f.write("-" * 40 + "\n")
        
#         try:
#             # 执行双因素重复测量方差分析
#             aov = AnovaRM(df, depvar=col, subject='Participant', within=['类型', '负荷'])
#             res = aov.fit()
#             f.write(str(res.summary()))
#         except Exception as e:
#             f.write(f"统计分析出错: {e}")
        
#         f.write("\n\n" + "="*50 + "\n\n")

# print(f"分析报告已保存为: {OUTPUT_REPORT}")