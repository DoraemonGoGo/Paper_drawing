import pandas as pd
import os


def extract_second_column_data(directory):
    second_column_data = []
    third_column_data = []
    five_column_data = []
    six_column_data = []

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            try:
                df = pd.read_csv(file_path)
                if len(df) >= 2 and df.shape[1] >= 6:
                    # 读取第二列从第二行开始的数据
                    column_data1 = df.iloc[0:, 1].tolist()
                    second_column_data.extend(column_data1)
                if len(df) >= 2 and df.shape[1] >= 6:
                    # 读取第二列从第二行开始的数据
                    column_data2 = df.iloc[0:, 2].tolist()
                    third_column_data.extend(column_data2)
                if len(df) >= 2 and df.shape[1] >= 6:
                    # 读取第二列从第二行开始的数据
                    column_data3 = df.iloc[0:, 4].tolist()
                    # print(column_data3[0])
                    five_column_data.extend(column_data3)
                if len(df) >= 2 and df.shape[1] >= 6:
                    # 读取第二列从第二行开始的数据
                    column_data4 = df.iloc[0:, 5].tolist()
                    six_column_data.extend(column_data4)
                    # print(len(second_column_data))
            except pd.errors.EmptyDataError:
                print(f"文件 {filename} 是空的，跳过")
            except Exception as e:
                print(f"处理文件 {filename} 时发生错误: {e}")

    return second_column_data, third_column_data, five_column_data, six_column_data


def store_data_in_target_file(directory, target_file):
    second_column_data, third_column_data, five_column_data, six_column_data = extract_second_column_data(directory)

    # if not os.path.exists(target_file) or os.path.getsize(target_file) == 0:
    #     # 如果目标文件不存在或为空，创建一个新的空的DataFrame并保存到CSV
    #     pd.DataFrame().to_csv(target_file, index=False)

    # target_df = pd.read_csv(target_file, encoding='latin1')
    target_df = pd.DataFrame()

    print(len(target_df))

    # 确保目标DataFrame有足够的行和列
    required_rows = len(second_column_data)
    while len(target_df) < required_rows:  # 加1是因为要从第二行开始填数据
        target_df = target_df.append(pd.Series(), ignore_index=True)
    while len(target_df.columns) < 4:
        target_df[len(target_df.columns)] = ''

    # 将数据存储到目标文件的第四列的第二行及以下的行中
    for i, data1 in enumerate(second_column_data):
        target_df.iat[i, 0] = data1  # i 对应第二行及以下, 第一列是索引0
    # 将数据存储到目标文件的第四列的第二行及以下的行中
    for i, data2 in enumerate(third_column_data):
        target_df.iat[i, 1] = data2  # i 对应第二行及以下, 第二列是索引1
    # 将数据存储到目标文件的第四列的第二行及以下的行中
    for i, data3 in enumerate(five_column_data):
        target_df.iat[i, 2] = data3  # i 对应第一行及以下, 第三列是索引2
    # 将数据存储到目标文件的第四列的第二行及以下的行中
    for i, data4 in enumerate(six_column_data):
        target_df.iat[i, 3] = data4  # i 对应第二行及以下, 第四列是索引3

    target_df.to_csv(target_file, index=False)
    print(f"数据已存储到 {target_file}")


# 调用函数并存储数据
directory_path = 'E:\\Desktop\\pycharm-study2'  # 替换为包含CSV文件的目录路径
target_file = 'E:\\Desktop\\pycharm-study2\\target_file_high.csv'  # 替换为目标文件的路径
store_data_in_target_file(directory_path, target_file)
