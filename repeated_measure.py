import pandas as pd

# 读取Excel文件
file_type = '.xlsx'
measure_value = '主要任务错误率'
task_type = 'Low'
file_path = 'E:/Desktop/paper/Study1_Data/' + task_type + ' Task/' + measure_value + task_type  # 替换为你的Excel文件路径
df = pd.read_excel(file_path + file_type)

# 按实验人员、角度和效果进行排序（确保数据顺序正确）
df = df.sort_values(by=['实验人员', '角度', '效果'])

# 重复测量数据格式转换
# 使用透视表将数据组织成新的格式
pivot_table1 = df.pivot_table(index='实验人员',
                              columns=['角度', '效果'],
                              values=measure_value)

# 将多重索引的列展平，并重排列顺序
pivot_table1.columns = [f'{effect}_{angle}' for angle, effect in pivot_table1.columns]

# 根据角度进行重新排列
ordered_columns1 = [f'{effect}_25' for effect in ['闪烁', '震动', '正常']] + [f'{effect}_45' for effect in
                                                                              ['闪烁', '震动', '正常']]
pivot_table1 = pivot_table1[ordered_columns1]

# 将结果保存到一个新的Excel文件
output_path1 = file_path + '重复测量' + file_type
pivot_table1.to_excel(output_path1)

print(f"数据已成功保存到 {output_path1}")


# 折线图数据格式转换
pivot_table2 = df.pivot_table(index='效果',
                              columns=['角度', '实验人员'],
                              values=measure_value)

pivot_table2.columns = [f'{angle}_{experimenter}' for angle, experimenter in pivot_table2.columns]
pivot_table2= pivot_table2.reindex(['闪烁', '震动', '正常'])
# 获取实际的列名
actual_columns_by_effect = pivot_table2.columns
# print(actual_columns_by_effect)
ordered_columns2 = [f'25_{i+1}' for i in range(12)] + [f'45_{i+1}' for i in range(12)]


pivot_table2 = pivot_table2[ordered_columns2]

output_path2 = file_path + '折线图' + file_type
pivot_table2.to_excel(output_path2)

print(f"数据已成功保存到 {output_path2}")
