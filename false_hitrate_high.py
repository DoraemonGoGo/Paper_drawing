import os
import glob
import csv
import pandas as pd

def calculate_ratio_for_file(filename):
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            lines = list(reader)

        # 确保文件有足够的行
        if len(lines) < 2:
            raise ValueError(f"{filename} 行数不足，无法计算")

        count_less_than_0 = 0
        non_zero_count = 0

        # 遍历每一行，跳过标题行
        for line in lines[1:]:  # 假设第一行为标题行
            if len(line) >= 5:  # 确保至少有五列
                value = float(line[4])  # 提取第五列的值
                if value < 0:
                    count_less_than_0 += 1  # 统计小于0的个数
                if value != 0:
                    non_zero_count += 1  # 统计非零数值的个数

        # 计算比值
        if non_zero_count == 0:
            return 0  # 避免除以零的情况
        ratio = count_less_than_0 / non_zero_count
        return ratio

    except Exception as e:
        return f"Error processing {filename}: {str(e)}"


# 获取文件夹中以low开头的csv文件
folder_path = 'E:/Desktop/Study1_Data/张博宣-8.6/High Task'  # 替换为你的文件夹路径
csv_files = glob.glob(os.path.join(folder_path, 'high*.csv'))

# 记录每个文件的比值
results = []

# 处理每个csv文件，计算比值并将结果保存到列表
for file in csv_files:
    ratio = calculate_ratio_for_file(file)
    results.append([os.path.basename(file), ratio])

# 创建 DataFrame 来保存结果
df = pd.DataFrame(results, columns=['Filename', 'Ratio'])

# 检查 DataFrame 有多少行
row_count = len(df)
print(row_count)
# 按照指定的行顺序重新排列
new_order = [4, 0, 2, 5, 1, 3]  # 你给定的顺序（注意这是基于0索引的顺序）
df_reordered = df.iloc[new_order]

# 保存重新排序后的文件
sorted_output_file = os.path.join(folder_path, 'falsehit_results.csv')
df_reordered.to_csv(sorted_output_file, index=False)

print(f"结果已按照顺序保存到 {sorted_output_file}")
