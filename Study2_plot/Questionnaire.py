import pandas as pd
import matplotlib.pyplot as plt

# 替换为你的文件路径
file_path = "E:/Desktop/paper/Study2_Data/Questionnaire.xlsx"  # 替换为实际的文件路径
# 读取 Excel 文件
df = pd.read_excel(file_path)
# 打印列名以确保名称正确
print("数据框的列名：", df.columns)
# 使用 replace 方法进行条件替换
df['条件'] = df['条件'].replace({'Gaze': 'Graded', 'Icon': 'Icon', 'Head': 'Head-up'})

# 计算每个条件下各个指标的平均值
mean_values = df.groupby('条件').mean().drop(columns=['实验人员'])

# 计算标准误差
sem_values = df.groupby('条件').sem().drop(columns=['实验人员'])

# 计算标准差
sd_values = df.groupby('条件').std().drop(columns=['实验人员'])

# 输出每个条件的标准差
print("\n各条件下的标准差：")
print(sd_values)
print("\n各条件下的平均值：")
print(mean_values)
# 绘制条形图
fig, ax = plt.subplots(figsize=(10, 6))

# 获取条件名称
conditions = mean_values.index
# 获取指标名称（包括总分）
metrics = mean_values.columns

# 条形图的宽度
bar_width = 0.2
# 条形图的X轴位置
x = range(len(metrics))
# colors = ['#2DA2FE', '#23D96E', '#FFBA60']
colors = ['#1f77b4', '#2ca02c', '#ff7f0e']

# 遍历每个条件，绘制对应的条形图
for i, condition in enumerate(conditions):
    ax.bar(
        [pos + i * bar_width for pos in x],
        mean_values.loc[condition],
        bar_width,
        label=condition,
        color=colors[i],
        yerr=sem_values.loc[condition],  # 添加误差线
        capsize=5,  # 设置误差线的长度
        alpha = 0.9  # 设置透明度为 0.9
    )

ax.spines['left'].set_bounds(0, 7)

# 设置X轴的刻度和标签
ax.set_xticks([pos + bar_width for pos in x])
ax.set_xticklabels(metrics, fontsize=14)

# 增加 y 轴刻度字体大小
ax.tick_params(axis='y', labelsize=14)

# 设置标题和Y轴标签
# ax.set_title('Notifications in VR Questionnaire', fontsize=14)
# ax.set_xlabel('指标', fontsize=12)
ax.set_ylabel('Score', fontsize=14)

# 添加显著性标记
def add_significance(ax, x1, x2, y, h, text):
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], color='black')
    ax.text((x1 + x2) * 0.5, y + h, text, ha='center', va='bottom', color='black')

# 在Noticeability那一列中添加显著性
# notice_index = 0  # Noticeability列的索引
# y_max = max(mean_values['Noticeability']) + max(sem_values['Noticeability'])  # 获取最大y值
# add_significance(ax, notice_index, notice_index + bar_width, y_max - 0.8, 0.1, '*')  # Head-up vs Graded
# add_significance(ax, notice_index + 2 * bar_width, notice_index + bar_width, y_max - 0.5, 0.1, '**')  # Head-up vs Icon
Intrusiveness_column = 'Intrusiveness'  # 替换为实际的列名
if Intrusiveness_column in mean_values.columns:
    notice_index = mean_values.columns.get_loc(Intrusiveness_column)
    y_max = max(mean_values[Intrusiveness_column]) + max(sem_values[Intrusiveness_column])

    # 在Intrusiveness那一列上添加显著性标记
    add_significance(ax, notice_index, notice_index + bar_width, y_max, 0.05, '*')  # Head-up vs Graded
    add_significance(ax, notice_index + bar_width, notice_index + 2 * bar_width, y_max + 0.35, 0.05,
                     '*')  # Head-up vs Icon

noticeability_column = 'Noticeability'  # 替换为实际的列名
if noticeability_column in mean_values.columns:
    notice_index = mean_values.columns.get_loc(noticeability_column)
    y_max = max(mean_values[noticeability_column]) + max(sem_values[noticeability_column])

    # 在Noticeability那一列上添加显著性标记
    add_significance(ax, notice_index, notice_index + 2 * bar_width, y_max + 0.35, 0.05, '**')  # Head-up vs Graded
    add_significance(ax, notice_index + bar_width, notice_index + 2 * bar_width, y_max, 0.05,
                     '***')  # Head-up vs Icon

Understandability_column = 'Understandability'  # 替换为实际的列名
if Understandability_column in mean_values.columns:
    notice_index = mean_values.columns.get_loc(Understandability_column)
    y_max = max(mean_values[Understandability_column]) + max(sem_values[Understandability_column])

    # 在Understandability那一列上添加显著性标记
    add_significance(ax, notice_index, notice_index + 2 * bar_width, y_max + 0.35, 0.05, '**')  # Head-up vs Graded
    add_significance(ax, notice_index + bar_width, notice_index + 2 * bar_width, y_max, 0.05,
                     '*')  # Head-up vs Icon

Urgency_column = 'Urgency'  # 替换为实际的列名
if Urgency_column in mean_values.columns:
    notice_index = mean_values.columns.get_loc(Urgency_column)
    y_max = max(mean_values[Urgency_column]) + max(sem_values[Urgency_column])

    # 在Urgency那一列上添加显著性标记
    add_significance(ax, notice_index, notice_index + bar_width, y_max + 0.43, 0.05, '**')  # Head-up vs Graded
    add_significance(ax, notice_index + bar_width, notice_index + 2 * bar_width, y_max + 0.08, 0.05,
                     '**')  # Head-up vs Icon

# 去掉顶部和右侧的边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 设置图例在底部并横向排列
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08), ncol=3, fontsize=13, frameon=False)

# 保存为 SVG 文件
plt.savefig("E:/Desktop/paper/Study2_Data/Questionnaire.jpg", format="jpg", bbox_inches='tight', dpi=300)  # 保存为 SVG 格式

# 调整图表布局并显示
plt.tight_layout()
plt.show()
