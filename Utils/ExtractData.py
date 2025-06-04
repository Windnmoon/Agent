import xlwings as xw


def extract_excel_data():
    input_path = 'raw_data/HSE资源费用统计总表_202504.xlsx'
    output_path = 'data/HSE资源费用整合表.xlsx'
    
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
        
        # 写入数据到目标位置 (第2-27行)
        output_sheet.range('A2').value = data
        
        # 保存输出文件
        output_wb.save(output_path)
        output_wb.close()
        # print(f"成功提取数据：{len(data)}行×{len(headers)}列")

if __name__ == "__main__":
    extract_excel_data()
    print("数据处理完成！output.xlsx已生成。")