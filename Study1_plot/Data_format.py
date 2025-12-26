import pandas as pd

# 假设你的文件是 Excel 文件，如果是 CSV 文件请使用 pd.read_csv()
file_path = 'E:/Desktop/Study1_Data/likert.xlsx'  # 请将路径替换为实际的文件路径
data = pd.read_excel(file_path)

# 使用 pivot_table 将数据转换为所需格式
pivoted_data = data.pivot_table(index=["通知角度", "显示方式"],
                                columns="实验人员",
                                values=["可察觉性", "舒适度", "感知效果"],
                                aggfunc='first')

# 将结果保存到新的 Excel 文件中
pivoted_data.to_excel('E:/Desktop/Study1_Data/formatted_output.xlsx')

# 或者可以直接查看转换后的数据
print(pivoted_data)
