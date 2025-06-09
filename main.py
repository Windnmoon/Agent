# 加载环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from Agent.ReAct import ReActAgent
from Models.Factory import ChatModelFactory
from Tools import *
from Tools.PythonTool import ExcelAnalyser, PlotTool
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from Utils.ClearFolder import *
from Utils.ExtractData import *

def launch_agent(agent: ReActAgent):
    human_icon = "\U0001F468"
    ai_icon = "\U0001F916"
    chat_history = ChatMessageHistory() # ChatMessageHistory：用于记录长时记忆（对话上下文），e.g.chat_history.add_user_message(task)， chat_history.add_ai_message(reply)

    delete_files_in_folder('./output')

    # extract_excel_data()

    while True:
        task = input(f"{ai_icon}：有什么可以帮您？\n{human_icon}：")
        if task.strip().lower() == "quit":
            break
        reply = agent.run(task, chat_history, verbose=True)
        print(f"{ai_icon}：{reply}\n")


def main():

    # 语言模型
    # llm = ChatModelFactory.get_model("gpt-4o-2024-05-13")
    llm = ChatModelFactory.get_model("deepseek")

    # 自定义工具集
    tools = [
        # document_qa_tool,
        # document_generation_tool,
        # email_tool,
        # excel_inspection_tool,
        directory_inspection_tool,
        finish_placeholder,
        ExcelAnalyser(
            llm=llm,
            knowledge_file="./prompts/knowledge/excel_knowledge.txt",
            prompt_file="./prompts/tools/excel_analyser.txt",
            verbose=True
        ).as_tool(),
        PlotTool(
            llm=llm,
            prompt_file="./prompts/tools/plot.txt",
            verbose=True
        ).as_tool()
    ]

    # 定义智能体
    agent = ReActAgent(
        llm=llm,
        tools=tools,
        work_dir="./data",
        main_prompt_file="./prompts/main/main.txt",
        knowledge_file = "./prompts/knowledge/excel_knowledge.txt",
        max_thought_steps=20,
    )

    # 运行智能体
    launch_agent(agent)


if __name__ == "__main__":
    main()
