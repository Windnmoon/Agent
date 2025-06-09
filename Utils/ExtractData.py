import xlwings as xw
import os
import re

def format_date(input_string):
    # 使用正则表达式匹配日期部分 '_202503'
    pattern = r'_(\d{4})(\d{2})'
    match = re.search(pattern, input_string)
    if match:
        # 提取年份和月份
        year = match.group(1)
        month = match.group(2)
        # 将月份转换为中文月份
        month_mapping = {
            '01': '1月',
            '02': '2月',
            '03': '3月',
            '04': '4月',
            '05': '5月',
            '06': '6月',
            '07': '7月',
            '08': '8月',
            '09': '9月',
            '10': '10月',
            '11': '11月',
            '12': '12月'
        }
        chinese_month = month_mapping.get(month)
        if chinese_month:
            # 拼接格式化的日期字符串
            formatted_date = f'{year}年{chinese_month}'
            return formatted_date
    # 如果没有匹配到日期部分，返回 None 或适当的错误消息
    return None

def extract_excel_data():
    raw_files_list = os.listdir('raw_data')
    for raw_file_name in raw_files_list:
        date_str = format_date(raw_file_name)
        input_path = f'raw_data/{raw_file_name}'
        output_path = f'data/HSE资源费用月表_{date_str}.xlsx'
        
        # # 打印路径以便调试
        # print(f"输入文件路径: {os.path.abspath(input_path)}")
        # print(f"输出文件路径: {os.path.abspath(output_path)}")


        # 打开输入工作簿并选择指定工作表
        with xw.Book(input_path) as input_wb:
            try:
                # 尝试获取名为"费用统计"的工作表
                input_sheet = input_wb.sheets["费用统计"]
            except KeyError:
                print("错误：HSE资源费用统计总表_202504.xlsx中找不到名为【费用统计】的工作表")
                return
            
            # 读取源数据范围 (第4-25行, C-G列)
            source_range = input_sheet.range('C4:G25')
            data = source_range.value
            
            # 创建输出工作簿
            output_wb = xw.Book()
            output_sheet = output_wb.sheets.active
            output_sheet.name = "费用统计"
            
            # 设置列标题
            headers = ['HSE团队名称', '磁盘账单（万元）', '本地机器账单（万元）', '云机器账单（万元）', '合计账单（万元）']
            output_sheet.range('A1').value = headers
            
            # 写入数据到目标位置 (第2-23行)
            output_sheet.range('A2').value = data

            row19 = output_sheet.range('19:19').value  # 获取整行数据
            row22 = output_sheet.range('22:22').value  # 获取整行数据

            # 处理数据：将第22行加到第19行（仅处理数值类型）
            new_row = []
            for i in range(len(row19)):
                # 如果两个值都是数字类型，则相加
                if isinstance(row19[i], (int, float)) and isinstance(row22[i], (int, float)):
                    new_row.append(row19[i] + row22[i])
                # 否则保留原始值（或处理其他逻辑）
                else:
                    new_row.append(row19[i])

            # 更新第19行数据
            output_sheet.range('19:19').value = new_row

            # 删除第22行（删除后下方行自动上移）
            output_sheet.range('22:22').api.EntireRow.Delete()

            # 保存输出文件
            output_wb.save(output_path)
            output_wb.close()
            # print(f"成功提取数据：{len(data)}行×{len(headers)}列")

if __name__ == "__main__":
    extract_excel_data()
    print("数据处理完成！output.xlsx已生成。")