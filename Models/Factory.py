import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

from langchain_openai import ChatOpenAI, OpenAIEmbeddings, AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_deepseek import ChatDeepSeek


class ChatModelFactory:
    model_params = {
        "temperature": 0,
        "seed": 42,
    }

    @classmethod
    def get_model(cls, model_name: str, use_azure: bool = False):
        if "deepseek" in model_name:

            '''
            deepseek-chat 模型指向 DeepSeek-V3-0324， 通过指定 model='deepseek-chat' 调用。
            deepseek-reasoner 模型指向 DeepSeek-R1-0528， 通过指定 model='deepseek-reasoner' 调用。
            '''
            return ChatDeepSeek(
                        model="deepseek-chat", # DeepSeek-V3-0324
                        # model="deepseek-reasoner", # DeepSeek-R1-0528
                        api_key="sk-78bbba8d1a214446958e01ac0d864657",
                        api_base="https://api.deepseek.com",
                        **cls.model_params
                        )
        
            # return ChatDeepSeek(
            #     model="deepseek-chat", # DeepSeek-V3-0324
            #     # model="deepseek-reasoner", # DeepSeek-R1-0528
            #     api_key="sk-78bbba8d1a214446958e01ac0d864657",
            #     api_base="https://api.deepseek.com",

            #     # api_key="sk-3bd31d29b8cc40d28e3b3cb45c71a24f",
            #     # api_base="http://hse-llm.enflame.cn/",
            #     **cls.model_params
            #     )
        
        elif model_name == "qwen":
            # 换成开源模型试试
            # https://siliconflow.cn/
            # 一个 Model-as-a-Service 平台
            # 可以通过与 OpenAI API 兼容的方式调用各种开源语言模型。
            # return ChatOpenAI(
            #     model="deepseek-ai/DeepSeek-V2-Chat",  # 模型名称
            #     openai_api_key=os.getenv("SILICONFLOW_API_KEY"),  # 在平台注册账号后获取
            #     openai_api_base="https://api.siliconflow.cn/v1",  # 平台 API 地址
            #     **cls.model_params,
            # )
            pass

    @classmethod
    def get_default_model(cls):
        return cls.get_model("deepseek")


class EmbeddingModelFactory:

    @classmethod
    def get_model(cls, model_name: str, use_azure: bool = False):
        if model_name.startswith("text-embedding"):
            if not use_azure:
                return OpenAIEmbeddings(model=model_name)
            else:
                return AzureOpenAIEmbeddings(
                    azure_deployment=model_name,
                    openai_api_version="2024-05-01-preview",
                )
        else:
            raise NotImplementedError(f"Model {model_name} not implemented.")

    @classmethod
    def get_default_model(cls):
        return cls.get_model("text-embedding-ada-002")
