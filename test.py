import xlwings as xw
import os
import csv

def excel_sheet_to_csv(input_file, sheet_name, output_file=None):
    """
    将Excel文件的指定工作表转换为CSV文件
    
    参数:
    input_file (str): 输入的Excel文件路径
    sheet_name (str): 要转换的工作表名称
    output_file (str): 输出的CSV文件路径(可选)
    """
    # 设置默认输出文件名
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + f"_{sheet_name}.csv"
    
    # 启动Excel应用
    with xw.App(visible=False) as app:
        # 打开工作簿
        wb = xw.Book(input_file)
        
        try:
            # 获取指定工作表
            sheet = wb.sheets[sheet_name]
            
            # 读取整个工作表数据
            data = sheet.used_range.value
            
            # 关闭工作簿(不保存)
            wb.close()
            
            # 写入CSV文件
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(data)
                
            print(f"转换成功! CSV文件已保存至: {output_file}")
            
        except KeyError:
            print(f"错误: 工作簿中不存在名为 '{sheet_name}' 的工作表")
            wb.close()
        except Exception as e:
            print(f"转换过程中发生错误: {str(e)}")
            wb.close()

# 使用示例
if __name__ == "__main__":
    # 替换为你的Excel文件路径
    excel_file = "C:/A_Work_Station/Work_Platform/A_Plan\Agent/raw_data/main_raw_data/HSE资源费用统计总表_202502.xlsx"
    sheet_name = "磁盘统计"
    
    # 执行转换
    excel_sheet_to_csv(excel_file, sheet_name)