import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False

# 读取CSV文件
file_path = 'E:/Desktop/paper/Study2_Data/reaction_secondary.xlsx'  # 请替换为实际文件名
df = pd.read_excel(file_path)

# 动态获取显示方式并排序 (按照 Graded, Heap-up/Head-up, Icon 的顺序)
existing_modes = df['显示方式'].unique()
# 定义优先顺序，兼容 Heap-up 和 Head-up（如果数据中有）
preferred_order = ['Graded', 'Heap-up', 'Head-up', 'Icon'] 
display_modes = [mode for mode in preferred_order if mode in existing_modes]
# 添加未在默认列表中的其他模式
for mode in existing_modes:
    if mode not in display_modes:
        display_modes.append(mode)

# 计算每种条件和负荷下的平均Recall、标准差(SD)和标准误差(SE)
average_recall = df.groupby(['显示方式', '负荷'])['反应时间'].agg(['mean', 'std', 'sem']).reset_index()

print("显示方式与负荷组合的平均值和标准差：")
for index, row in average_recall.iterrows():
    print(f"显示方式: {row['显示方式']}, 负荷: {row['负荷']}, 平均值: {row['mean']:.4f}, 标准差: {row['std']:.4f}")

# 计算Heavy和Light负荷的平均值和标准差
heavy_light_recall = df[df['显示方式'].isin(display_modes)]  # 只选择Heavy和Light负荷
heavy_light_recall = heavy_light_recall.groupby(['显示方式'])['反应时间'].agg(['mean', 'std']).reset_index()

print("\nHeavy和Light负荷下的平均值和标准差：")
for index, row in heavy_light_recall.iterrows():
    print(f"显示方式: {row['显示方式']}, 平均值: {row['mean']:.4f}, 标准差: {row['std']:.4f}")
# 创建一个图
fig, ax = plt.subplots(figsize=(4, 5))

# 设置x轴的偏移量
offset = 0.1
conditions = np.arange(len(display_modes))

# 自动检测负荷列的唯一值
available_loads = df['负荷'].unique()
if len(available_loads) >= 2:
    if 'Heavy' in available_loads and 'Light' in available_loads:
        loads_to_plot = ['Heavy', 'Light']
    elif 'High' in available_loads and 'Low' in available_loads:
        loads_to_plot = ['High', 'Low']
    else:
        loads_to_plot = list(available_loads)[:2]
else:
    loads_to_plot = list(available_loads)

# 根据检测到的负荷设置颜色和标记
colors = {}
markers = {}
color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
marker_palette = ['o', 's', '^', 'D']

for idx, load in enumerate(loads_to_plot):
    colors[load] = color_palette[idx % len(color_palette)]
    markers[load] = marker_palette[idx % len(marker_palette)]

label_map = {'Heavy': '重负荷', 'Light': '轻负荷'}

# 为Heavy和Light的平均Recall绘制两条折线，并添加误差线
min_val = float('inf') # 记录数据最小值，用于调整坐标轴
max_val = float('-inf')

for i, load in enumerate(loads_to_plot):
    # 按照 display_modes 的顺序提取数据，确保绘图对齐
    subset = average_recall[average_recall['负荷'] == load].set_index('显示方式').reindex(display_modes).reset_index()
    
    # 记录数据范围 (包含误差线)
    if not subset['mean'].dropna().empty:
        # 填充NaN的误差为0，防止计算结果为NaN
        current_sems = subset['sem'].fillna(0)
        current_max = (subset['mean'] + current_sems).max()
        current_min = (subset['mean'] - current_sems).min()
        
        if not pd.isna(current_max):
            max_val = max(max_val, current_max)
        if not pd.isna(current_min):
            min_val = min(min_val, current_min)
    
    # 计算偏移后的x轴位置
    x_positions = conditions + (i - 0.5) * offset
    # plt.errorbar(x_positions, subset['mean'], yerr=subset['sem'], marker='o', label=load, capsize=5, color=colors[load])
    if load in colors:
        label_text = label_map.get(load, load)
        plt.errorbar(x_positions, subset['mean'], yerr=subset['sem'], marker=markers[load], label=label_text, capsize=5, color=colors[load])

# 动态计算条件数量
num_conditions = len(display_modes)

# 自动调整Y轴
if min_val != float('inf'):
    # 计算合适的刻度间隔
    data_range = max_val - min_val
    if data_range == 0: data_range = 0.1
    
    # 初步确定步长量级
    step = 10 ** np.floor(np.log10(data_range))
    # 根据归一化后的范围调整步长
    norm_range = data_range / step
    if norm_range < 1.5:
        step /= 5
    elif norm_range < 3:
        step /= 2
        
    # 计算刻度范围
    y_min_tick = np.floor(min_val / step) * step
    y_max_tick = np.ceil(max_val / step) * step
    
    # 生成刻度
    ticks = np.arange(y_min_tick, y_max_tick + step/1000, step)
    
    ax.set_yticks(ticks)
    ax.set_ylim(ticks[0], ticks[-1])
    ax.spines['left'].set_bounds(ticks[0], ticks[-1])
    
    # 设置底部坐标轴位置 - 向下偏移一个步长的25%
    ax.spines['bottom'].set_position(('data', ticks[0] - step * 0.25))
else:
    # 默认值，以防没数据
    ax.set_ylim(0, 1)

ax.set_xlim(-0.5, num_conditions - 0.5) # 动态设置 xlim
# 调整 x 轴刻度的字体大小
ax.tick_params(axis='x', labelsize=16)  # 设置 x 轴刻度标签字体大小为 20
ax.tick_params(axis='y', labelsize=16)  # 设置 x 轴刻度标签字体大小为 20

# 自动生成 Y 轴刻度(可选，或者让 matplotlib 自动处理)
# ax.set_yticks(...) 

# 强制让底部的 X 轴只显示点之间的范围
val_bounds_max = num_conditions - 1 if num_conditions > 0 else 1
ax.spines['bottom'].set_bounds(0, val_bounds_max)


# 添加标题和标签
plt.ylabel('反应时间(s)', fontsize=16, fontweight='bold')
# ax.text(0.4, -0.15, '(d)', transform=ax.transAxes, ha='center', va='top', fontsize=18, fontweight='normal', fontname='Times New Roman')
ax.text(0.4, -0.2, '(d) 次要任务反应时间', transform=ax.transAxes, ha='center', va='top', fontsize=17, fontweight='normal')

# 设置X轴的刻度和标签
ax.set_xticks(np.arange(num_conditions))
# 替换标签中的 Heap-up 为 Head-up (如果是 Heap-up 的话)
display_labels = ['Head-up' if x == 'Heap-up' else x for x in display_modes]
ax.set_xticklabels(display_labels, fontsize=16)

# 去掉顶部和右侧的边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 设置图例，去掉框线
# 将图例移动到左上角，或者使用 bbox_to_anchor 微调位置
ax.legend(loc='upper left', frameon=False, fontsize=16)

# 保存为矢量图
plt.savefig("E:/Desktop/paper/Study2_Data/reaction_secondary.jpg", format="jpg", bbox_inches='tight', dpi=300)  # 保存为 SVG 矢量图格式

# 显示图表
plt.grid(False)
# 调整布局，确保边距足够显示
plt.tight_layout()
plt.show()


