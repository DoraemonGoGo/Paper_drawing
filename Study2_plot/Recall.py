import os
import pandas as pd

def extract_and_save_data(folder_path, output_file):
    # 创建一个空的列表，用于存储文件名和对应的值
    results = []

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        # 检查文件是否以"question"开头
        if file_name.startswith("question"):
            file_path = os.path.join(folder_path, file_name)
            # 尝试不同的编码读取文件
            for encoding in ['utf-8', 'ISO-8859-1', 'GBK']:
                try:
                    # 读取文件中的数据，假设文件是CSV格式
                    df = pd.read_csv(file_path, header=None, encoding=encoding)
                    # 提取第一行第二列的值
                    value = df.iloc[0, 5]  # 第二列的索引是1（从0开始）
                    # 将文件名和对应的值添加到结果列表
                    results.append([file_name, value])
                    break  # 如果成功读取并添加，跳出编码尝试循环
                except Exception as e:
                    print(f"尝试使用编码 {encoding} 读取文件 {file_name} 失败: {e}")

    # 将结果保存到输出文件（CSV格式），第一列为文件名，第二列为对应的值
    results_df = pd.DataFrame(results, columns=['文件名', '数据'])
    results_df.to_csv(output_file, index=False, encoding='utf-8-sig')

# 使用示例
folder_path = "E:/Desktop/Study2_Data/贾诺1-9.6"
output_file = folder_path + "/recall.csv"
# extract_first_row_fifth_column(folder_path, output_file)
extract_and_save_data(folder_path, output_file)
print("处理完成，结果已保存到", output_file)
