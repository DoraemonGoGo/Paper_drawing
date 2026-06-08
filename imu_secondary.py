import pandas as pd
import os

# ================= 配置部分 =================
# 输入文件名 (请修改为你实际的文件名)
input_file = 'E:\\Desktop\\paper\\gesture_study\\handle\\responses_LowTask.csv'  # 如果是 csv 文件，请改为 'data.csv'

# 输出文件名
output_file = 'E:\\Desktop\\paper\\gesture_study\\handle\\notistatic_low.csv'
# ===========================================

def main():
    # 1. 读取文件
    print(f"正在读取文件: {input_file} ...")
    
    try:
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        elif input_file.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(input_file)
        else:
            print("错误: 不支持的文件格式。请使用 .csv 或 .xlsx 文件。")
            return
    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_file}，请确保文件在当前目录下。")
        return

    # 2. 数据预处理
    # 确保 Response 列中的空白字符被正确识别为 NaN (空值)
    # 有时候 Excel 里的空单元格会被读成空字符串 "" 或空格 " "
    if 'Response' in df.columns:
        df['Response'] = df['Response'].replace(r'^\s*$', pd.NA, regex=True)
    else:
        print("错误: 数据表中找不到 'Response' 列。")
        return

    # 3. 统计计算
    results = []

    # (1) Response 为空的统计 TotalTime 的平均值
    empty_response_df = df[df['Response'].isna()]
    if not empty_response_df.empty:
        avg_total_time = empty_response_df['TotalTime'].mean()
        results.append({'统计项目': 'Response为空: TotalTime平均值', '数值': avg_total_time})
    else:
        results.append({'统计项目': 'Response为空: TotalTime平均值', '数值': 0})

    # (2) Response 不空的统计
    valid_response_df = df[df['Response'].notna()]
    
    if not valid_response_df.empty:
        # ReactionTime 平均值
        avg_reaction_time = valid_response_df['ReactionTime'].mean()
        results.append({'统计项目': 'Response不为空: ReactionTime平均值', '数值': avg_reaction_time})
        
        # (TotalTime - ReactionTime) 平均值
        # 计算差值列
        time_diff = valid_response_df['TotalTime'] - valid_response_df['ReactionTime']
        avg_diff = time_diff.mean()
        results.append({'统计项目': 'Response不为空: (TotalTime - ReactionTime)平均值', '数值': avg_diff})
    else:
        results.append({'统计项目': 'Response不为空: ReactionTime平均值', '数值': 0})
        results.append({'统计项目': 'Response不为空: (TotalTime - ReactionTime)平均值', '数值': 0})

    # 4. 生成结果文件
    result_df = pd.DataFrame(results)
    
    # 保存为 CSV，使用 utf-8-sig 编码防止中文乱码
    result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print("-" * 30)
    print("统计完成！")
    print(result_df)
    print("-" * 30)
    print(f"结果已保存至: {output_file}")

if __name__ == "__main__":
    main()