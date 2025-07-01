### 项目介绍

此项目可利用AI大模型的能力进行统计图表的绘制。

### 环境配置

```bash
pip install -r requirements.txt
```

### 运行

在项目根目录下执行

```bash
python main.py
```

### 提问示例

- SoCDV & SYSIPDV团队，2025年2月至2025年5月期间，横轴月份，纵轴合计账单（万元），画出柱状图

- HSE所有团队2025年2月至2025年5月期间，各团队的累计合计账单从大到小分别是多少，画出柱状图 

- 2025年2月至2025年5月期间，在本地机器账单这一项的总费用上，list出的所有团队从大到小的排名，并据此画出柱状图

- 画出HSE的pdxlarge_hosts集群在2025年2月至2025年5月期间的总节点数的整体统计图

- 画出SOCDE团队2025年2月至2025年5月期间的slot利用率统计图（横轴以周为单位）

- 2025年2月至2025年5月期间，slot利用率最高与最低的团队分别是谁

- 2025年2月至2025年5月期间，哪些团队至少有一个周的slot利用率低于10%，需要整改

### 文件说明

main.py：主程序文件

Agent文件夹：

——Action.py：规定智能体所执行工具的结构，具体是由工具名name和工具输入参数args两各部分组成

——React.py：对下图中的逻辑框架进行实现

<img src="README.assets\image-20250622141251506.png" alt="image-20250622141251506" style="zoom: 50%;" />

data文件夹：存放脚本预处理后的简洁表格

raw_data文件夹：存放脚本预处理前的原始表格

Models文件夹：

——Factory.py：用于获取模型，此处调用了DeepSeek API接口

output文件夹：图片等结果的输出文件夹

prompts文件夹：存储所有提示词模板，以及有关表格的knowledge

——knowledge.txt：存放有关表格的knowledge

——main.txt：主提示词模板，每一轮思考调用的即是此模板

——excel_analyser.txt：执行表格分析工具时会调用此模板

——plot.txt：执行画图工具时会调用此模板

Tools文件夹：存放大模型可选用的所有工具

——ExcelTool.py：探查表格内容的工具（打印表格sheet名、打印表格前n行，流程优化后此工具用不上）

——FileTool.py：探查data文件夹中文件名的工具

——PythonTool.py：写python代码并执行的工具，内含写代码分析表格内容的工具，与写代码画图的工具，这两个工具都有对应的promt模板文件

Utils文件夹：存放各类脚本

——CallbackHandlers.py：实现回调功能，用于在上述逻辑框架的特定阶段执行结束时打印相关信息

——ClearFolder.py：每次开始执行任务时，清空output文件夹中上次任务的输出

——ExtractData.py：原始Excel表格的预处理脚本，在raw_data文件夹中有新文件添加时执行

——PrintUtils.py：彩色打印函数，上述逻辑框架在不同阶段用不同颜色打印

examples.txt：用户提问的样例

requirements.txt：环境必要依赖

requirements_long.txt：加长版环境依赖

test.py：用于开发时做测试











