from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class Action(BaseModel):
    # 定义一个名为name的属性，类型为str（字符串），并使用Field函数为其添加描述信息"Tool name"
    name: str = Field(description="Tool name") 
     #定义一个名为args的属性，类型为Optional[Dict[str, Any]]，表示一个可选的字典，其中键为字符串，值为任意类型。使用Field函数为其添加描述信息
    args: Optional[Dict[str, Any]] = Field(description="Tool input arguments, containing arguments names and values") 
   
    # 定义__str__方法，用于将Action对象转换为易读的字符串表示，方便调试和日志记录。
    def __str__(self):
        ret = f"Action(name={self.name}"
        if self.args:
            for k, v in self.args.items():
                ret += f", {k}={v}"
        ret += ")"
        return ret
    
    '''
    __str__方法的用途演示：

    创建一个Action对象
    action = Action(name="example_tool", args={"arg1": "value1", "arg2": 42})

    打印Action对象
    print(action)
    等同于print(str(action))
    输出: Action(name=example_tool, arg1=value1, arg2=42)


    str() 函数
    str() 是Python内置的一个函数，用于将对象转换为字符串表示。
    当 str() 函数被调用时，它会查找对象的 __str__() 方法并执行它。如果对象没有定义 __str__() 方法，它会回退到调用对象的 __repr__() 方法。

    '''
