import os
import pandas as pd


def process_files_in_folder(folder_path):
    # 获取文件夹中所有文件名
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # 存储计算结果
    results = []

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)

        # 读取CSV文件，跳过第一行（列名），假设数据从第二行开始
        df = pd.read_csv(file_path, header=0)  # header=0表示第一行是列名

        # 如果文件以low开头，处理第四列
        if file_name.startswith('low'):
            col = df.iloc[1:, 3]  # 从第二行开始读取第四列（索引3）
            positive_sum = col[col > 0].sum()
            positive_count = (col > 0).sum()
            negative_count = (col < 0).sum()
            non_zero_count = (col != 0).sum()

            if positive_count > 0:
                positive_avg = positive_sum / positive_count
            else:
                positive_avg = 0

            if non_zero_count > 0:
                negative_ratio = negative_count / non_zero_count
            else:
                negative_ratio = 0

            results.append((file_name, positive_avg, negative_ratio))

        # 如果文件以high开头，处理第五列
        elif file_name.startswith('high'):
            col = df.iloc[1:, 4]  # 从第二行开始读取第五列（索引4）
            positive_sum = col[col > 0].sum()
            positive_count = (col > 0).sum()
            negative_count = (col < 0).sum()
            non_zero_count = (col != 0).sum()

            if positive_count > 0:
                positive_avg = positive_sum / positive_count
            else:
                positive_avg = 0

            if non_zero_count > 0:
                negative_ratio = negative_count / non_zero_count
            else:
                negative_ratio = 0

            results.append((file_name, positive_avg, negative_ratio))

    # 将结果保存到新的文件中
    output_df = pd.DataFrame(results, columns=["File Name", "Positive Average", "Negative Ratio"])
    output_file_path = os.path.join(folder_path, "processed_results.csv")
    output_df.to_csv(output_file_path, index=False)
    print(f"Results saved to {output_file_path}")


# 使用方法
folder_path = 'E:\\Desktop\\pycharm-study'  # 替换成实际文件夹路径
process_files_in_folder(folder_path)
