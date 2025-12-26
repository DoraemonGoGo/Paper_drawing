import pandas as pd

# 读取Excel文件
file_type = '.xlsx'
measure_value = '主要任务反应时间'
task_type = 'High'
file_path = 'E:/Desktop/Study1_Data/' + task_type + ' Task/' + measure_value + task_type  # 替换为你的Excel文件路径
df = pd.read_excel(file_path + file_type)

# 按实验人员、角度和效果进行排序（确保数据顺序正确）
df = df.sort_values(by=['实验人员', '角度', '效果'])

# 使用透视表将数据组织成新的格式
pivot_table = df.pivot_table(index='效果',
                             columns=['角度', '实验人员'],
                             values=measure_value)

# 将多重索引的列展平，并重排列顺序
pivot_table.columns = [f'{angle}_{experimenter}' for angle, experimenter in pivot_table.columns]

# 根据角度进行重新排列
ordered_columns = [f'25_{i+1}' for i in range(12)] + [f'45_{i+1}' for i in range(12)]
pivot_table = pivot_table[ordered_columns]

# 将结果保存到一个新的Excel文件
output_path = file_path + '折线图' + file_type
pivot_table.to_excel(output_path)

print(f"数据已成功保存到 {output_path}")
