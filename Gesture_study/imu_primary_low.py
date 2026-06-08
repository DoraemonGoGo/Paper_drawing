import pandas as pd

def process_csv(file_path, output_path):
    # 读取CSV文件到DataFrame
    df = pd.read_csv(file_path)
    
    # 检查列数是否至少为4
    if df.shape[1] >= 4:
        # 提取第4列（索引3）
        fourth_column = df.iloc[:, 3]
        
        # 过滤出大于0的值
        positive_values = fourth_column[fourth_column > 0]
        
        # 计算其平均值（如果有值，否则为None）
        if not positive_values.empty:
            average = positive_values.mean()
        else:
            average = None
        
        # 计算小于0的值的数量作为错误率（比例）
        count_less_than_0 = (fourth_column < 0).sum()
        non_zero_count = (fourth_column != 0).sum()
        if non_zero_count == 0:
            error_rate = 0
        else:
            error_rate = count_less_than_0 / non_zero_count
        
        # 创建结果DataFrame并保存到新文件
        result_df = pd.DataFrame({
            'Average': [average],
            'Error Rate': [error_rate]
        })
        result_df.to_csv(output_path, index=False)
        print(f"处理结果已保存到 {output_path}")
    else:
        print("CSV文件列数不足4，无法处理。")

# 示例调用（请根据需要修改路径）
input_file = 'E:\Desktop\gesture_study\handle\low_task.csv'  # 替换为实际输入CSV文件路径
output_file = 'E:\Desktop\gesture_study\handle\lowstatic.csv'  # 替换为实际输出CSV文件路径
process_csv(input_file, output_file)