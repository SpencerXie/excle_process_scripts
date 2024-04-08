import pandas as pd
import traceback
import sys


def merge_excel_files(input_list, output_file, output_list):
    # 创建一个空的DataFrame来存储合并的数据
    merged_data = pd.DataFrame()

    # 遍历输入列表
    for item in input_list:
        for file_name, sheet_info in item.items():
            for sheet_name, columns in sheet_info.items():
                try:
                    # 如果sheet_name为空字符串，使用None作为sheet_name的值
                    if sheet_name == '':
                        sheet_name = 0
                    # 读取Excel文件的特定工作表
                    data = pd.read_excel(file_name, sheet_name=sheet_name)
                    # 为输入数据添加一个空列，用于匹配输入为空的case
                    data[''] = ''
                    # 按照output_list的顺序重新排列列
                    data = data[columns]
                    data_col_len = len(data.columns)
                    data.columns = output_list[:data_col_len]
                    # 检查并填充缺失的列
                    for col in output_list:
                        if col not in data.columns:
                            data[col] = None
                    # 添加一列来存储文件名
                    data['SourceFile'] = file_name
                    # 将数据添加到merged_data中
                    merged_data = pd.concat([merged_data, data])
                except Exception as e:
                    print(f"在处理文件 {file_name} 的 {sheet_name} 时发生错误: {e}")
                    traceback.print_exc()  # 打印出错误的详细信息，包括错误发生的行号
                    sys.exit(1)  # 终止程序，返回一个非零的退出状态，表示程序遇到了错误

    # 更改列名
    merged_data.columns = output_list + ['SourceFile']

    # 将合并的数据写入Excel文件
    save_large_data_to_excel(merged_data, output_file)


def save_large_data_to_excel(data, output_file):
    max_rows = 1048576
    num_parts = len(data) // max_rows + 1

    for i in range(num_parts):
        part_data = data[i * max_rows:(i + 1) * max_rows]
        part_file = output_file.replace('.xlsx', f'_part{i + 1}.xlsx')
        part_data.to_excel(part_file, index=False)


# 使用示例
input_list = [{'file1.xlsx': {'': ['a1', 'a2', '', '名字']}},
              {'file2.xlsx': {'Sheet1': ['b1', 'b2', 'b3', 'b4'], 'Sheet2': ['b6', 'b7', 'b8', 'b9']}},
              {'file3.xlsx': {'Sheet1': ['c1', 'c2', 'c3', 'c4', 'c5']}}]
output_list = ['out1', 'out2', 'out3', 'out4', '哈哈']
merge_excel_files(input_list, 'output1.xlsx', output_list)
