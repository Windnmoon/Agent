import warnings
warnings.filterwarnings("ignore")

from langchain.tools import StructuredTool
from .FileTool import list_files_in_directory
from .FinishTool import finish
from .ExcelTool import get_first_n_rows

excel_inspection_tool = StructuredTool.from_function(
    func=get_first_n_rows,
    name="InspectExcel",
    description="探查表格文件的内容和结构，展示它的列名和前n行，n默认为3",
) # got it

directory_inspection_tool = StructuredTool.from_function(
    func=list_files_in_directory,
    name="ListDirectory",
    description="探查文件夹的内容和结构，展示它的文件名和文件夹名",
) # got it

finish_placeholder = StructuredTool.from_function(
    func=finish,
    name="FINISH",
    description="结束任务，将最终答案返回"
) # got it

"""
总结：Tools 工具就是执行一个任务，可以有返回值，也可以没有返回值
"""
