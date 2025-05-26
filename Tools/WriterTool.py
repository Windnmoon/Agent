from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from Models.Factory import ChatModelFactory


def write(query: str, verbose=False):
    """按用户要求撰写文档"""
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "你是专业的文档写手。你根据客户的要求，写一份文档。输出中文。"),
            HumanMessagePromptTemplate.from_template("{query}"),
        ]
    )

    llm = ChatModelFactory.get_default_model()

    chain = {"query": RunnablePassthrough()} | template | llm | StrOutputParser()
    # RunnablePassthrough 是一个特殊的可运行对象，它的作用是 直接将输入传递到下一个组件，不做任何修改。在这里，它确保输入的 query 字符串能够被传递到下一个步骤（即模板）

    return chain.invoke(query)
    # chain.invoke(query) 是执行整个 LangChain 链式调用的入口点。它接收用户的输入 query，依次经过链中的各个组件（输入传递、提示词生成、语言模型处理、输出解析），最终返回处理后的字符串结果。


if __name__ == "__main__":
    print(write("写一封邮件给张三，内容是：你好，我是李四。"))
