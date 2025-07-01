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
        output_path = f'data/HSE资源费用等综合信息月表_{date_str}.xlsx'


        # 创建输出工作簿
        output_wb = xw.Book()
        output_sheet4 = output_wb.sheets.active
        output_sheet4.name = "mem使用情况统计"
        output_sheet3 = output_wb.sheets.add("slot使用情况统计")
        output_sheet2 = output_wb.sheets.add("集群统计")
        output_sheet1 = output_wb.sheets.add("费用统计")
        
        # # 打印路径以便调试
        # print(f"输入文件路径: {os.path.abspath(input_path)}")
        # print(f"输出文件路径: {os.path.abspath(output_path)}")


        # 打开输入工作簿并选择指定工作表
        with xw.Book(input_path) as input_wb:
            #——————————————————————————————"费用统计"的工作表——————————————————————————————
            try:
                # 尝试获取名为"费用统计"的工作表
                input_sheet = input_wb.sheets["费用统计"]
            except KeyError:
                print("错误：HSE资源费用统计总表_202504.xlsx中找不到名为【费用统计】的工作表")
                return
            
            # 读取源数据范围 (第4-25行, C-G列)
            source_range = input_sheet.range('C4:G25')
            data = source_range.value
            
            # 设置列标题
            headers = ['HSE团队名称', '磁盘账单（万元）', '本地机器账单（万元）', '云机器账单（万元）', '合计账单（万元）']
            output_sheet1.range('A1').value = headers
            
            # 写入数据到目标位置 (第2-23行)
            output_sheet1.range('A2').value = data

            row19 = output_sheet1.range('19:19').value  # 获取整行数据
            row22 = output_sheet1.range('22:22').value  # 获取整行数据

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
            output_sheet1.range('19:19').value = new_row

            # 删除第22行（删除后下方行自动上移）
            output_sheet1.range('22:22').api.EntireRow.Delete()


            #——————————————————————————————"集群统计"的工作表——————————————————————————————
            try:
                # 尝试获取名为"集群统计"的工作表
                input_sheet = input_wb.sheets["集群统计"]
            except KeyError:
                print("错误：HSE资源费用统计总表_202504.xlsx中找不到名为【集群统计】的工作表")
                return
            
            last_col_index = input_sheet.used_range.last_cell.column
            four_week_last_index = 47
            five_week_last_index = 56

            # 设置列标题
            headers = ['HSE集群名称', '总节点数（台）']
            output_sheet2.range('A1').value = headers

            if last_col_index == four_week_last_index:
                # 读取源数据范围 
                source_range = input_sheet.range('A4:A11')
                data = source_range.value

                # 写入到目标位置
                output_sheet2.range('A2').options(transpose=True).value = data

                # 处理4-11行
                for row in range(4, 12):
                    # 定义要读取的列（P=16, U=21, Z=26, AE=31）
                    columns = [16, 21, 26, 31]
                    total = 0
                    
                    # 计算每行指定列的总和
                    for col in columns:
                        cell_value = input_sheet.cells(row, col).value
                        if isinstance(cell_value, (int, float)):
                            total += cell_value
        
                    # 将结果写入目标表B列
                    output_sheet2.cells(row-2, 2).value = total  # B列=列索引2
            
            elif last_col_index == five_week_last_index:
                # 读取源数据范围
                source_range = input_sheet.range('A4:A11')
                data = source_range.value

                # 写入到目标位置
                output_sheet2.range('A2').options(transpose=True).value = data

                # 处理4-11行
                for row in range(4, 12):
                    # 定义要读取的列（P=16, U=21, Z=26, AE=31, AJ=36）
                    columns = [16, 21, 26, 31, 36]
                    total = 0
                    
                    # 计算每行指定列的总和
                    for col in columns:
                        cell_value = input_sheet.cells(row, col).value
                        if isinstance(cell_value, (int, float)):
                            total += cell_value
        
                    # 将结果写入目标表B列
                    output_sheet2.cells(row-2, 2).value = total  # B列=列索引2

            else:
                print("Error: column num of sheet['集群统计'] is unexpected")


            #——————————————————————————————"slot使用情况统计"的工作表——————————————————————————————
            try:
                # 尝试获取名为"前端运行数据统计"的工作表
                input_sheet = input_wb.sheets["前端运行数据统计"]
            except KeyError:
                print("错误：HSE资源费用统计总表_202504.xlsx中找不到名为【前端运行数据统计】的工作表")
                return
            
            last_col_index = input_sheet.used_range.last_cell.column
            four_week_last_index = 20
            five_week_last_index = 21
            five_week_four_valid_flag = (last_col_index == five_week_last_index and not isinstance(input_sheet.range('U3').value, (int, float)))

            if last_col_index == four_week_last_index or five_week_four_valid_flag:
                # 设置列标题
                headers = ['HSE团队名称', 'slot利用率Week1', 'slot利用率Week2', 'slot利用率Week3', 'slot利用率Week4', 'slot申请占比Week1', 'slot申请占比Week2', 'slot申请占比Week3', 'slot申请占比Week4']
                output_sheet3.range('A1').value = headers

                # 读取源数据范围 
                source_range = input_sheet.range('N3:N14')
                data = source_range.value

                # 写入到目标位置 
                output_sheet3.range('A2').options(transpose=True).value = data


                if last_col_index == four_week_last_index: 
                    source_range = input_sheet.range('T16:T27') # slot利用率
                    data = source_range.value
                    output_sheet3.range('B2').options(transpose=True).value = data

                    source_range = input_sheet.range('S16:S27')
                    data = source_range.value
                    output_sheet3.range('C2').options(transpose=True).value = data

                    source_range = input_sheet.range('R16:R27')
                    data = source_range.value
                    output_sheet3.range('D2').options(transpose=True).value = data

                    source_range = input_sheet.range('Q16:Q27')
                    data = source_range.value
                    output_sheet3.range('E2').options(transpose=True).value = data

                    source_range = input_sheet.range('T3:T14') # slot申请占比
                    data = source_range.value
                    output_sheet3.range('F2').options(transpose=True).value = data

                    source_range = input_sheet.range('S3:S14')
                    data = source_range.value
                    output_sheet3.range('G2').options(transpose=True).value = data

                    source_range = input_sheet.range('R3:R14')
                    data = source_range.value
                    output_sheet3.range('H2').options(transpose=True).value = data

                    source_range = input_sheet.range('Q3:Q14')
                    data = source_range.value
                    output_sheet3.range('I2').options(transpose=True).value = data
                
                if five_week_four_valid_flag:
                    source_range = input_sheet.range('Q16:T27') # slot利用率
                    data = source_range.value
                    output_sheet3.range('B2').value = data

                    source_range = input_sheet.range('Q3:T14') # slot申请占比
                    data = source_range.value
                    output_sheet3.range('F2').value = data

            if last_col_index == five_week_last_index and not five_week_four_valid_flag:
                # 设置列标题
                headers = ['HSE团队名称', 'slot利用率Week1', 'slot利用率Week2', 'slot利用率Week3', 'slot利用率Week4', 'slot利用率Week5', 'slot申请占比Week1', 'slot申请占比Week2', 'slot申请占比Week3', 'slot申请占比Week4', 'slot申请占比Week5',]
                output_sheet3.range('A1').value = headers

                # 读取源数据范围 
                source_range = input_sheet.range('N3:N14')
                data = source_range.value

                # 写入到目标位置 
                output_sheet3.range('A2').options(transpose=True).value = data

                # 读取源数据范围 
                source_range = input_sheet.range('Q16:U27') # slot利用率
                data = source_range.value
                # 写入到目标位置
                output_sheet3.range('B2').value = data

                # 读取源数据范围 
                source_range = input_sheet.range('Q3:U14') # slot申请占比
                data = source_range.value
                # 写入到目标位置
                output_sheet3.range('G2').value = data

            
            #——————————————————————————————"mem使用情况统计"的工作表——————————————————————————————
            try:
                # 尝试获取名为"中端运行数据统计"的工作表
                input_sheet = input_wb.sheets["中端运行数据统计"]
            except KeyError:
                print("错误：HSE资源费用统计总表_202504.xlsx中找不到名为【中端运行数据统计】的工作表")
                return
            
            last_col_index = input_sheet.used_range.last_cell.column
            four_week_last_index = 20
            five_week_last_index = 21
            five_week_four_valid_flag = (last_col_index == five_week_last_index and not isinstance(input_sheet.range('U3').value, (int, float)))

            if last_col_index == four_week_last_index or five_week_four_valid_flag:
                # 设置列标题
                headers = ['HSE团队名称', 'mem利用率Week1', 'mem利用率Week2', 'mem利用率Week3', 'mem利用率Week4', 'mem申请占比Week1', 'mem申请占比Week2', 'mem申请占比Week3', 'mem申请占比Week4']
                output_sheet4.range('A1').value = headers

                # 读取源数据范围 
                source_range = input_sheet.range('N3:N7')
                data = source_range.value

                # 写入到目标位置 
                output_sheet4.range('A2').options(transpose=True).value = data


                if last_col_index == four_week_last_index: 
                    source_range = input_sheet.range('T16:T20') # mem利用率
                    data = source_range.value
                    output_sheet4.range('B2').options(transpose=True).value = data

                    source_range = input_sheet.range('S16:S20')
                    data = source_range.value
                    output_sheet4.range('C2').options(transpose=True).value = data

                    source_range = input_sheet.range('R16:R20')
                    data = source_range.value
                    output_sheet4.range('D2').options(transpose=True).value = data

                    source_range = input_sheet.range('Q16:Q20')
                    data = source_range.value
                    output_sheet4.range('E2').options(transpose=True).value = data

                    source_range = input_sheet.range('T3:T7') # slot申请占比
                    data = source_range.value
                    output_sheet4.range('F2').options(transpose=True).value = data

                    source_range = input_sheet.range('S3:S7')
                    data = source_range.value
                    output_sheet4.range('G2').options(transpose=True).value = data

                    source_range = input_sheet.range('R3:R7')
                    data = source_range.value
                    output_sheet4.range('H2').options(transpose=True).value = data

                    source_range = input_sheet.range('Q3:Q7')
                    data = source_range.value
                    output_sheet4.range('I2').options(transpose=True).value = data
                
                if five_week_four_valid_flag:
                    source_range = input_sheet.range('Q16:T20') # slot利用率
                    data = source_range.value
                    output_sheet4.range('B2').value = data

                    source_range = input_sheet.range('Q3:T7') # slot申请占比
                    data = source_range.value
                    output_sheet4.range('F2').value = data

            if last_col_index == five_week_last_index and not five_week_four_valid_flag:
                # 设置列标题
                headers = ['HSE团队名称', 'mem利用率Week1', 'mem利用率Week2', 'mem利用率Week3', 'mem利用率Week4', 'mem利用率Week5', 'mem申请占比Week1', 'mem申请占比Week2', 'mem申请占比Week3', 'mem申请占比Week4', 'mem申请占比Week5',]
                output_sheet4.range('A1').value = headers

                # 读取源数据范围 
                source_range = input_sheet.range('N3:N7')
                data = source_range.value

                # 写入到目标位置 
                output_sheet4.range('A2').options(transpose=True).value = data

                # 读取源数据范围 
                source_range = input_sheet.range('Q16:U20') # slot利用率
                data = source_range.value
                # 写入到目标位置
                output_sheet4.range('B2').value = data

                # 读取源数据范围 
                source_range = input_sheet.range('Q3:U7') # slot申请占比
                data = source_range.value
                # 写入到目标位置
                output_sheet4.range('G2').value = data


             # 保存输出文件
            output_wb.save(output_path)
            output_wb.close()


if __name__ == "__main__":
    extract_excel_data()
    print("数据处理完成！output.xlsx已生成。")