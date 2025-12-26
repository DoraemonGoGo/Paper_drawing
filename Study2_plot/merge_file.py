import os
import pandas as pd

def merge_files_by_name(folders, file_names, output_folder):
    """
    从多个文件夹中合并多个文件名对应的文件，并将每个合并后的结果分别保存。

    参数:
    - folders: 包含所有文件夹路径的列表
    - file_names: 需要合并的文件名列表
    - output_folder: 输出合并文件的保存文件夹
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in file_names:
        # 用于存储当前文件名对应的所有文件的数据
        data_frames = []

        # 遍历每个文件夹，读取文件数据
        for folder in folders:
            file_path = os.path.join(folder, file_name)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                data_frames.append(df)
            else:
                print(f"文件 {file_path} 不存在，跳过。")

        # 合并所有数据
        if data_frames:
            merged_df = pd.concat(data_frames, ignore_index=True)
            # 保存合并后的数据到输出文件
            output_file = os.path.join(output_folder, f'merged_{file_name}')
            merged_df.to_csv(output_file, index=False)
            print(f"合并后的文件已保存到 {output_file}")
        else:
            print(f"没有找到任何文件进行合并：{file_name}")

# 示例用法
folders = ['E:/Desktop/Study2_Data/吴昌坤5-9.10', 'E:/Desktop/Study2_Data/张博宣6-9.10',
           'E:/Desktop/Study2_Data/田家明7-9.11', 'E:/Desktop/Study2_Data/高星8-9.12',
           'E:/Desktop/Study2_Data/马康硕9-9.13']  # 替换为实际的文件夹路径
file_names = ['eye_tracking_data_HighTask_Blink.csv', 'eye_tracking_data_HighTask_cameraTrack.csv',
              'eye_tracking_data_HighTask_iconDisplay.csv', 'eye_tracking_data_LowTask_Blink.csv',
              'eye_tracking_data_LowTask_cameraTrack.csv', 'eye_tracking_data_LowTask_iconDisplay.csv']  # 替换为实际的文件名列表
output_folder = 'E:/Desktop/Study2_Data/merged_files'  # 合并文件的输出文件夹

merge_files_by_name(folders, file_names, output_folder)
