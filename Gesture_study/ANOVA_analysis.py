import pandas as pd
from statsmodels.stats.anova import AnovaRM

# 1. 读取数据
df = pd.read_csv('E:\\Desktop\\gesture_study\\static_data.csv')

# 2. 定义需要分析的指标
metrics = ['主任务反应时间', '主任务错误率', '一阶段操作时间', '二阶段操作时间']

# ================= 生成方差分析 (ANOVA) 表格 =================
anova_list = []
for metric in metrics:
    try:
        # 运行 ANOVA
        aov = AnovaRM(df, depvar=metric, subject='Participant', within=['类型', '负荷'])
        res = aov.fit()
        
        # 提取结果表
        temp_df = res.anova_table.copy()
        temp_df.insert(0, 'Metric', metric) # 插入指标列
        temp_df.reset_index(inplace=True)   # 将索引(因子名)转为列
        temp_df.rename(columns={'index': 'Factor', 'Pr > F': 'p-value'}, inplace=True)
        
        anova_list.append(temp_df)
    except Exception as e:
        print(f"分析 {metric} 时出错: {e}")

# 合并并保存 ANOVA 结果
final_anova_df = pd.concat(anova_list, ignore_index=True)
final_anova_df.to_csv('Experiment_ANOVA_Results.csv', index=False, encoding='utf-8-sig')
print("ANOVA 结果已保存至: Experiment_ANOVA_Results.csv")

# ================= 生成描述性统计 (Descriptive) 表格 =================
# 按组计算均值和标准差
desc_df = df.groupby(['类型', '负荷'])[metrics].agg(['mean', 'std'])

# 扁平化列名 (例如: ('主任务反应时间', 'mean') -> '主任务反应时间_mean')
desc_df.columns = [f"{col[0]}_{col[1]}" for col in desc_df.columns]
desc_df.reset_index(inplace=True)

# 保存描述性统计结果
desc_df.to_csv('Experiment_Descriptive_Stats.csv', index=False, encoding='utf-8-sig')
print("描述性统计已保存至: Experiment_Descriptive_Stats.csv")