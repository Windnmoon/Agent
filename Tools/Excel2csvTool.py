import xlwings as xw
import csv
import io

def excel_sheet_to_csv(input_file_list: list, sheet_name: str) -> str:
    """
    将Excel文件的指定工作表转换为CSV字符串
    
    参数:
    input_file (list): 输入的Excel文件名列表
    sheet_name (str): 要转换的工作表名称
    """

    result = ''
    
    for input_file_path in input_file_list:
        output = io.StringIO()
        input_file_name = input_file_path.split('/')[-1]
        with xw.Book(input_file_path) as wb:
            try:
                # 获取指定工作表
                sheet = wb.sheets[sheet_name]
                
                # 读取整个工作表数据
                data = sheet.used_range.value

                # 将数据写入内存中的CSV文件
                writer = csv.writer(output)
                writer.writerows(data)

                result += f"{input_file_name}文件的'{sheet_name}'工作表内容:\n{output.getvalue()}\n"

            except KeyError:
                result += f"错误: 工作簿中不存在名为 '{sheet_name}' 的工作表"
                wb.close()
            except Exception as e:
                result += f"转换过程中发生错误: {str(e)}"
                wb.close()
                
    return result

# 使用示例
if __name__ == "__main__":
    # 替换为你的Excel文件路径
    excel_file = ["HSE各项综合信息月表_2025年2月.xlsx"]
    sheet_name = "费用统计"
    
    # 执行转换
    excel_sheet_to_csv(excel_file, sheet_name)
    