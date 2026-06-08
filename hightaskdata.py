import pandas as pd
import os


def calculate_statistics(directory):
    task_averages = []
    task_filenames = []
    task_error_rates = []

    reaction_averages = []
    reaction_filenames = []
    reaction_error_rates = []

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)

            if filename.startswith("high"):
                # 处理low开头的文件
                if df.shape[1] >= 5:
                    fourth_column = df.iloc[:, 4]

                    # 过滤出大于0的值
                    positive_values = fourth_column[fourth_column > 0]

                    # 计算和与计数
                    if not positive_values.empty:
                        average = positive_values.mean()
                    else:
                        average = None
                    # 计算小于0的值的个数
                    error_count = (fourth_column < 0).sum()

                    task_averages.append(average)
                    task_filenames.append(filename)
                    task_error_rates.append(error_count)

            elif filename.startswith("reaction"):
                # 处理reaction开头的文件
                if df.shape[1] >= 3:
                    fourth_column = df.iloc[:, 2]

                    # 过滤出大于0的值
                    positive_values = fourth_column[fourth_column > 0]

                    # 计算和与计数
                    if not positive_values.empty:
                        average = positive_values.mean()
                    else:
                        average = None
                    # 计算小于0的值的个数
                    error_count = (fourth_column < 0).sum()

                    reaction_filenames.append(filename)
                    reaction_averages.append(average)
                    reaction_error_rates.append(error_count)

    return (task_filenames, task_averages, task_error_rates), (reaction_filenames, reaction_averages, reaction_error_rates)


def save_statistics_to_csv(directory, output_file):
    (task_filenames, task_averages, task_error_rates), (
    reaction_filenames, reaction_averages, reaction_error_rates) = calculate_statistics(directory)

    # 创建一个DataFrame保存结果
    result_df = pd.DataFrame({
        'High Filename': task_filenames,
        'High Average': task_averages,
        'High Error Rate': task_error_rates,
        'Reaction Filename': reaction_filenames,
        'Reaction Average': reaction_averages,
        'Reaction Error Rate': reaction_error_rates
    })

    print(len(result_df))
    # 重新排列从第二行到第七行的数据
    new_order = [4, 0, 2, 5, 1, 3]
    reordered_df = result_df.iloc[0:6].reset_index(drop=True).iloc[new_order].reset_index(drop=True)

    # 读取输入的实验者序号并加入到文件名中
    user_input = input("请输入实验者序号：")
    output_file = output_file.replace('.csv', f'_{user_input}.csv')

    # 将结果保存到新的CSV文件中
    reordered_df.to_csv(output_file, index=False)
    print(f"统计结果已保存到 {output_file}")


# 调用函数并保存结果
directory_path = 'E:\\Desktop\\paper\\pycharm-study'  # 替换为包含CSV文件的目录路径
output_file = 'E:\\Desktop\\paper\\pycharm-study\\highstatistic.csv'
save_statistics_to_csv(directory_path, output_file)
