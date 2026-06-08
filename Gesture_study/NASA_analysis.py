import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.anova import AnovaRM

# ================= 配置区域 =================
INPUT_FILE = 'E:\\Desktop\\gesture_study\\NASA_TLX_3.csv'
FONT_FAMILY = ['SimSun'] # Windows用户使用SimHei，Mac用户请尝试 ['Arial Unicode MS']
# ===========================================

# 1. 读取数据
try:
    df = pd.read_csv(INPUT_FILE)
    df['负荷'] = df['负荷'].map({'轻': '轻负荷', '重': '重负荷'})
except FileNotFoundError:
    print(f"错误：找不到文件 {INPUT_FILE}")
    exit()

# 设置绘图风格
sns.set_context("paper", font_scale=1.5)
sns.set_style("ticks", {'axes.grid': True, 'grid.linestyle': '--', 'grid.alpha': 0.3})
plt.rcParams['font.sans-serif'] = FONT_FAMILY
plt.rcParams['axes.unicode_minus'] = False

# ---------------------------------------------------------
# 图表 1: NASA-TLX 总分对比 (核心结果)
# ---------------------------------------------------------
plt.figure(figsize=(8, 6))

# 绘制柱状图
ax1 = sns.barplot(
    x='负荷', y='NASA_TLX_Score', hue='类型', data=df,
    palette="Set2", capsize=0.1, errorbar=('ci', 95),
    edgecolor=".3", linewidth=1.5
)

# 美化
plt.title('NASA-TLX 总负荷评分对比', fontweight='bold', fontsize=16, pad=15)
plt.ylabel('NASA-TLX 总分 (0-10)', fontsize=16)
plt.xlabel('', fontsize=16)
ax1.tick_params(axis='both', labelsize=16)
plt.ylim(0, 10) # 假设是10分制，如果是100分制请改为100
plt.legend(title='交互方式', fontsize=16, title_fontsize=16)
sns.despine()

plt.tight_layout()
plt.savefig('NASA_TLX_3_Total.png', dpi=300)
print("图表 1 已保存: NASA_TLX_3_Total.png")

# ---------------------------------------------------------
# 图表 2: 六大维度子量表详情 (深入分析)
# ---------------------------------------------------------
# 数据转换：将宽表转换为长表，方便画图
subscales = ['Mental Demand', 'Physical Demand', 'Temporal Demand', 'Performance', 'Effort', 'Frustration']
df_melted = df.melt(id_vars=['Participant', '类型', '负荷'], value_vars=subscales, 
                    var_name='维度', value_name='评分')

plt.figure(figsize=(14, 7))

# 绘制柱状图
ax2 = sns.barplot(
    x='维度', y='评分', hue='类型', data=df_melted,
    palette=['#4c72b0', '#c44e52'], capsize=0.05, errorbar=('ci', 95),
    edgecolor=".3", linewidth=1
)

# 美化
plt.title('NASA-TLX 六大维度评分详情', fontweight='bold', fontsize=16, pad=15)
plt.ylabel('评分 (Score)', fontsize=16)
plt.xlabel('', fontsize=16)
ax2.tick_params(axis='both', labelsize=16)
plt.ylim(0, 10) # 同上，根据实际分制调整
plt.xticks(rotation=15) # 稍微倾斜标签以防重叠
plt.legend(title='交互方式', loc='upper left', bbox_to_anchor=(1, 1), fontsize=14, title_fontsize=14) # 图例放外侧
sns.despine()

plt.tight_layout()
plt.savefig('NASA_TLX_3_Subscales.png', dpi=300)
print("图表 2 已保存: NASA_TLX_3_Subscales.png")

# ---------------------------------------------------------
# 附带：自动输出统计分析结果
# ---------------------------------------------------------
print("\n=== NASA-TLX 总分统计分析结果 ===")
try:
    aov = AnovaRM(df, depvar='NASA_TLX_Score', subject='Participant', within=['类型', '负荷'])
    res = aov.fit()
    print(res.summary())
except Exception as e:
    print(f"统计分析出错: {e}")