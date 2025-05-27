import re
from typing import List, Tuple

from langchain_community.chat_message_histories.in_memory import ChatMessageHistory # got it
from langchain_core.language_models.chat_models import BaseChatModel # got it
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser # got it
from langchain.schema.output_parser import StrOutputParser # got it
from langchain.tools.base import BaseTool # got it
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # got it
from langchain_core.tools import  render_text_description  # got it
from langchain_core.prompts import HumanMessagePromptTemplate # got it

from pydantic import ValidationError
from Agent.Action import Action
from Utils.CallbackHandlers import *


class ReActAgent:
    """AutoGPT：基于Langchain实现"""

    @staticmethod # 静态方法可以通过类名直接调用，也可以通过实例调用（尽管不推荐后者），由于没有self或cls参数，静态方法无法直接访问实例或类的属性
    def __format_thought_observation(thought: str, action: Action, observation: str) -> str:
        # 将全部JSON代码块替换为空
        ret = re.sub(r'```json(.*?)```', '', thought, flags=re.DOTALL)
        ret += "\n" + str(action) + "\n返回结果:\n" + observation
        return ret

    @staticmethod
    def __extract_json_action(text: str) -> str | None:
        # 匹配最后出现的JSON代码块
        json_pattern = re.compile(r'```json(.*?)```', re.DOTALL) # 此行需要查langchain文档
        matches = json_pattern.findall(text)
        if matches:
            last_json_str = matches[-1]
            return last_json_str
        return None

    def __init__(
            self,
            llm: BaseChatModel,
            tools: List[BaseTool], # tools的类型为一个List，其中每个元素都是BaseTool类型或其子类型的实例
            work_dir: str,
            main_prompt_file: str,
            max_thought_steps: Optional[int] = 10,
    ):
        self.llm = llm
        self.tools = tools
        self.work_dir = work_dir
        self.main_prompt_file = main_prompt_file
        self.max_thought_steps = max_thought_steps

        self.verbose_handler = ColoredPrintHandler(color=THOUGHT_COLOR)

        # OutputFixingParser： 如果输出格式不正确，尝试修复
        self.output_parser = PydanticOutputParser(pydantic_object=Action) # PydanticOutputParser：创建一个输出解析器，用于将模型的输出解析为指定的 Pydantic 模型 Action
        self.robust_parser = OutputFixingParser.from_llm(
            parser=self.output_parser,
            llm=llm
        ) # 一个更健壮的输出解析器，能够在解析失败时尝试自动修复输出。它使用基础解析器 PydanticOutputParser 和语言模型 llm 来生成新的提示并重新解析输出


        self.__init_prompt_templates()
        self.__init_chains()

    def __init_prompt_templates(self):
        with open(self.main_prompt_file, 'r', encoding='utf-8') as f:
            self.prompt = ChatPromptTemplate.from_messages( # 用类方法from_messages创建prompt模板
                [
                    MessagesPlaceholder(variable_name="chat_history"), # MessagesPlaceholder：用来存放对话历史
                    HumanMessagePromptTemplate.from_template(f.read()), # HumanMessagePromptTemplate：存放用户写的prompt模板
                                                                        # f.read()的返回值为self.main_prompt_file文件的字符串内容
                ]
            ).partial( # partial方法用来填充from_messages所创造实例中的槽位
                work_dir=self.work_dir,
                tools=render_text_description(self.tools), # render_text_description将工具列表转换为文本描述，以便在提示模板中使用，使模型能够了解可用的工具及其功能
                tool_names=','.join([tool.name for tool in self.tools]),
                format_instructions=self.output_parser.get_format_instructions(), # get_format_instructions：获取输出解析器的格式说明，并将其传递给提示模板。这些格式说明告诉模型如何生成符合输出解析器要求的输出，从而确保模型的输出能够被正确解析和使用
            )


    def __init_chains(self):
        # 主流程的chain
        self.main_chain = (self.prompt | self.llm | StrOutputParser()) # StrOutputParser：只是简单地将输出转换为字符串类型

    # BaseTool 是 LangChain 中定义工具的基类，它提供了一些核心属性和方法，用于工具的输入参数验证、输出格式定义以及工具的同步和异步执行。通过从 BaseTool 子类化，可以创建自定义的工具，以满足特定的需求
    def __find_tool(self, tool_name: str) -> Optional[BaseTool]:
        for tool in self.tools:
            if tool.name == tool_name:
                return tool
        return None

    def __step(self,
               task,
               short_term_memory,
               chat_history,
               verbose=False
               ) -> Tuple[Action, str]: # 应该返回一个元组，第一个元素的类型是 Action，第二个元素的类型是 str

        """执行一步思考"""

        inputs = { # 执行一步思考的输入为：用户问题，长时记忆与短时记忆
            "input": task,
            "agent_scratchpad": "\n".join(short_term_memory), # scratchpad意为：便签簿
            "chat_history": chat_history.messages,
        }

        config = {
            "callbacks": [self.verbose_handler]
            if verbose else []
        }
        response = ""

        # self.main_chain 作为实现了 Runnable 接口的实例，具备 stream 方法。stream 方法是 Runnable 接口中定义的一个方法，用于流式处理输出。它允许逐步生成和处理输出，而不是一次性返回完整的结果。这种方法特别适用于需要处理大量输出或希望逐步显示响应的场景，例如在聊天应用或实时数据处理中
        for s in self.main_chain.stream(inputs, config=config): 
            response += s

        # 提取JSON代码块
        json_action = self.__extract_json_action(response)
        # 带容错的解析
        action = self.robust_parser.parse(
            json_action if json_action else response
        ) # parse 方法是 LangChain 中输出解析器（Output Parser）的核心方法，用于将语言模型的输出解析为某种结构化格式。它接受语言模型生成的文本输出作为参数，返回结构化的数据类型，从而实现了对输出的验证和处理

        return action, response

    def __exec_action(self, action: Action) -> str:
        # 查找工具
        tool = self.__find_tool(action.name)
        if tool is None:
            observation = (
                f"Error: 找不到工具或指令 '{action.name}'. "
                f"请从提供的工具/指令列表中选择，请确保按对顶格式输出。"
            )
        else:
            try:
                # 执行工具
                observation = tool.run(action.args)
            except ValidationError as e:
                # 工具的入参异常
                observation = (
                    f"Validation Error in args: {str(e)}, args: {action.args}"
                )
            except Exception as e:
                # 工具执行异常
                observation = f"Error: {str(e)}, {type(e).__name__}, args: {action.args}"

        return observation

    def run(
            self,
            task: str,
            chat_history: ChatMessageHistory, # ChatMessageHistory：用于记录长时记忆（对话上下文），e.g.chat_history.add_user_message(task)， chat_history.add_ai_message(reply)
            verbose=False
    ) -> str:
        """
        运行智能体
        :param task: 用户任务
        :param chat_history: 对话上下文（长时记忆）
        :param verbose: 是否显示详细信息
        """
        # 初始化短时记忆: 记录执行工具得到的结果
        short_term_memory = []

        # 思考步数
        thought_step_count = 0

        reply = ""

        # 开始逐步思考
        while thought_step_count < self.max_thought_steps:
            if verbose:
                self.verbose_handler.on_thought_start(thought_step_count) # 打印：开始第几轮思考

            # 执行一步思考
            action, response = self.__step(
                task=task,
                short_term_memory=short_term_memory,
                chat_history=chat_history,
                verbose=verbose,
            )

            # 如果是结束指令，执行最后一步
            if action.name == "FINISH":
                reply = self.__exec_action(action)
                break

            # 执行动作
            observation = self.__exec_action(action)

            if verbose:
                self.verbose_handler.on_tool_end(observation) # 将observation内容用指定颜色打印出来

            # 更新短时记忆
            short_term_memory.append(
                self.__format_thought_observation(
                    response, action, observation
                )
            ) # 包含了一步思考的结果，执行的action名称，执行结果

            thought_step_count += 1

        if thought_step_count >= self.max_thought_steps:
            # 如果思考步数达到上限，返回错误信息
            reply = "抱歉，我没能完成您的任务。"

        # 更新长时记忆
        chat_history.add_user_message(task)
        chat_history.add_ai_message(reply)
        return reply
    

    '''
        下划线__的含义
        有些方法以 __ 开头，如 __exec_action，表示这些方法是类的私有方法，仅供内部使用，不希望被子类或外部代码直接调用。而有些方法不以 __ 开头，如 run，表示这些方法是类的公共方法，是类的对外接口，可以被其他代码直接调用。
    '''
