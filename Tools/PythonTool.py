import re
from typing import Union, Dict

from langchain.tools import StructuredTool
from langchain_core.language_models import BaseChatModel, BaseLanguageModel
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate

from Models.Factory import ChatModelFactory
from Utils.CallbackHandlers import ColoredPrintHandler
from Utils.PrintUtils import CODE_COLOR
from langchain_openai import ChatOpenAI
from .ExcelTool import get_first_n_rows, get_column_names, get_csv_first_n_rows
from langchain_experimental.utilities import PythonREPL


class PythonCodeParser(BaseOutputParser):
    """从OpenAI返回的文本中提取Python代码。"""

    @staticmethod
    def __remove_marked_lines(input_str: str) -> str:
        lines = input_str.strip().split('\n')
        if lines and lines[0].strip().startswith('```'):
            del lines[0]
        if lines and lines[-1].strip().startswith('```'):
            del lines[-1]

        ans = '\n'.join(lines)
        return ans

    def parse(self, text: str) -> str:
        # 使用正则表达式找到所有的Python代码块
        python_code_blocks = re.findall(r'```python\n(.*?)\n```', text, re.DOTALL)
        # 从re返回结果提取出Python代码文本
        python_code = None
        if len(python_code_blocks) > 0:
            python_code = python_code_blocks[0]
            python_code = self.__remove_marked_lines(python_code)
        return python_code


class ExcelAnalyser:
    """
    从Excel文件中提取信息或分析数据（基于 Python 代码实现）。
    输入中必须包含文件的完整路径和具体分析方式和分析依据等。
    输入的文件路径可能是一个或多个，均以字典的形式给出。
    """

    def __init__(
            self,
            llm: Union[BaseLanguageModel, BaseChatModel], # Union[BaseLanguageModel, BaseChatModel] 表示 llm 参数可以接收 BaseLanguageModel 类型或 BaseChatModel 类型的实例。
            knowledge_file="./prompts/knowledge/excel_knowledge.txt",
            prompt_file="./prompts/tools/excel_analyser.txt",
            verbose=False
    ):
        self.llm = llm
        self.prompt = PromptTemplate.from_file(prompt_file, encoding='utf-8')
        self.verbose = verbose
        self.knowledge_file = knowledge_file
        self.verbose_handler = ColoredPrintHandler(CODE_COLOR)

    def analyse(self, query, filename: Dict):

        """分析一个结构化文件（例如excel文件）的内容。"""

        with open(self.knowledge_file, 'r', encoding='utf-8') as f:
            knowledge = f.read()

        code_parser = PythonCodeParser()
        chain = self.prompt | self.llm | StrOutputParser()

        response = ""

        for c in chain.stream({
            "query": query,
            "filename": filename,
            "knowledge": knowledge
        }, config={
            "callbacks": [
                self.verbose_handler
            ] if self.verbose else []
        }):
            response += c

        code = code_parser.parse(response)

        if code:
            ans = query+"\n"+PythonREPL().run(code) # PythonREPL 是一个类，用于在 Python 的交互式解释器（REPL）中执行代码。run(code) 方法接收一个字符串参数 code，表示要执行的 Python 代码，并返回代码的执行结果。
            return ans
        else:
            return "没有找到可执行的Python代码"

    def as_tool(self):
        return StructuredTool.from_function(
            func=self.analyse,
            name="AnalyseExcel",
            description=self.__class__.__doc__.replace("\n", ""), # self.__class__ 获取当前对象的类，即 ExcelAnalyser 类本身。__doc__ 是 Python 中的特殊属性，用于获取类或函数的文档字符串（docstring），即class ExcelAnalyser下面一行的字符串
        )
    

class PlotTool:
    """
    根据绘图数据信息：plot_information进行画图（基于 Python 代码实现）。
    输入中必须包含具体的画图要求和绘图所依赖的数据：plot_information。
    绘图数据信息：plot_information以自然语言的形式呈现。
    """

    def __init__(
            self,
            llm: Union[BaseLanguageModel, BaseChatModel], # Union[BaseLanguageModel, BaseChatModel] 表示 llm 参数可以接收 BaseLanguageModel 类型或 BaseChatModel 类型的实例。
            prompt_file="./prompts/tools/plot.txt",
            verbose=False
    ):
        self.llm = llm
        self.prompt = PromptTemplate.from_file(prompt_file, encoding='utf-8')
        self.verbose = verbose
        self.verbose_handler = ColoredPrintHandler(CODE_COLOR)

    def agent_plot(self, query, plot_information: str):

        """
        根据绘图数据信息：plot_information进行画图（基于 Python 代码实现）。
        输入中必须包含具体的画图要求和绘图所依赖的数据：plot_information。
        绘图数据信息：plot_information以自然语言的形式呈现。
        """
        
        code_parser = PythonCodeParser()
        chain = self.prompt | self.llm | StrOutputParser()

        response = ""

        for c in chain.stream({
            "query": query,
            "plot_information": plot_information
        }, config={
            "callbacks": [
                self.verbose_handler
            ] if self.verbose else []
        }):
            response += c

        code = code_parser.parse(response)

        if code:
            ans = query+"\n"+PythonREPL().run(code) # PythonREPL 是一个类，用于在 Python 的交互式解释器（REPL）中执行代码。run(code) 方法接收一个字符串参数 code，表示要执行的 Python 代码，并返回代码的执行结果。
            return ans
        else:
            return "没有找到可执行的Python代码"

    def as_tool(self):
        return StructuredTool.from_function(
            func=self.agent_plot,
            name="plot_with_csv",
            description=self.__class__.__doc__.replace("\n", ""), # self.__class__ 获取当前对象的类，即 ExcelAnalyser 类本身。__doc__ 是 Python 中的特殊属性，用于获取类或函数的文档字符串（docstring），即class ExcelAnalyser下面一行的字符串
        )


if __name__ == "__main__":
    print(ExcelAnalyser(
        ChatModelFactory.get_model("gpt-4o"),
    ).analyse(
        query="8月销售额",
        filename="../data/2023年8月-9月销售记录.xlsx"
    ))
