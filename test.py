# from langchain_experimental.utilities import PythonREPL
# import subprocess


# code1 = '''import matplotlib.pyplot as plt
# import matplotlib as mpl

# # 设置中文显示
# mpl.rcParams['font.family'] = 'Microsoft YaHei'
# mpl.rcParams['axes.unicode_minus'] = False

# # 数据准备
# months = ['2月', '3月', '4月', '5月']
# socdv_bills = [7.247585177719607, 7.7273729196760215, 6.444900552660393, 6.886357735638013]
# dce_bills = [3.3076259267955965, 2.4437099236636137, 2.4145680608624502, 2.5226468643304454]

# # 创建图表
# fig, ax = plt.subplots(figsize=(10, 6))

# # 设置柱状图位置和宽度
# x = range(len(months))
# width = 0.35

# # 绘制柱状图
# rects1 = ax.bar([i - width/2 for i in x], socdv_bills, width, label='SOCDV团队', color='royalblue')
# rects2 = ax.bar([i + width/2 for i in x], dce_bills, width, label='DCE团队', color='orange')

# # 添加数据标签
# def add_labels(rects):
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate(f'{height:.2f}',
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom',
#                     color='black')

# add_labels(rects1)
# add_labels(rects2)

# # 添加标题和标签
# ax.set_title('2025年度HSE SOCDV和DCE团队的月度账单合计统计图')
# ax.set_xlabel('月份')
# ax.set_ylabel('合计账单（万元）')
# ax.set_xticks(x)
# ax.set_xticklabels(months)
# ax.legend()

# # 设置网格线
# ax.set_axisbelow(True)
# ax.grid(True, axis='y', linestyle='--', alpha=1.0)

# # 添加水印
# plt.figtext(
#     0.9, 0.02, 
#     'Enflame A plan', 
#     ha='right', 
#     fontsize=10, 
#     color='gray', 
#     alpha=0.7,
#     style='italic'
# )

# # 调整布局
# plt.tight_layout()

# # 保存图像
# plt.savefig('output/2025_HSE_team_bills.png', dpi=300, bbox_inches='tight')
# plt.savefig('output/2025_HSE_team_bills.svg', format='svg', bbox_inches='tight')

# print("已成功绘制图像")'''

# code2 = '''print("心想事成")'''
# print("大吉大利")

# # ans = PythonREPL().run(code1)
# # print(ans)

# ans = subprocess.run(
#     ["python", "-c", code1],  # -c 表示执行代码字符串
#     capture_output=True,
#     text=True
# )

# print(ans.stdout)
# print("吉星高照")




import subprocess

code = '''import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置中文显示
mpl.rcParams['font.family'] = 'Microsoft YaHei'
mpl.rcParams['axes.unicode_minus'] = False

# 数据准备
months = ['2月', '3月', '4月', '5月']
socdv_bills = [7.247585177719607, 7.7273729196760215, 6.444900552660393, 6.886357735638013]
dce_bills = [3.3076259267955965, 2.4437099236636137, 2.4145680608624502, 2.5226468643304454]

# 创建图表
fig, ax = plt.subplots(figsize=(10, 6))

# 设置柱状图位置和宽度
x = range(len(months))
width = 0.35

# 绘制柱状图
rects1 = ax.bar([i - width/2 for i in x], socdv_bills, width, label='SOCDV团队', color='royalblue')
rects2 = ax.bar([i + width/2 for i in x], dce_bills, width, label='DCE团队', color='orange')

# 添加数据标签
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    color='black')

add_labels(rects1)
add_labels(rects2)

# 添加标题和标签
ax.set_title('2025年度HSE SOCDV和DCE团队的月度账单合计统计图')
ax.set_xlabel('月份')
ax.set_ylabel('合计账单（万元）')
ax.set_xticks(x)
ax.set_xticklabels(months)
ax.legend()

# 设置网格线
ax.set_axisbelow(True)
ax.grid(True, axis='y', linestyle='--', alpha=1.0)

# 添加水印
plt.figtext(
    0.9, 0.02, 
    'Enflame A plan', 
    ha='right', 
    fontsize=10, 
    color='gray', 
    alpha=0.7,
    style='italic'
)

# 调整布局
plt.tight_layout()

# 保存图像
plt.savefig('output/2025_HSE_team_bills.png', dpi=300, bbox_inches='tight')
plt.savefig('output/2025_HSE_team_bills.svg', format='svg', bbox_inches='tight')

print("已成功绘制图像")'''

ans = subprocess.run(
    ["python", "-c", code],  # -c 表示执行代码字符串
    capture_output=True,
    text=True
)

print(ans.stdout)





# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import os

# # # 设置中文字体
# # mpl.rcParams['font.family'] = 'Microsoft YaHei'
# # mpl.rcParams['axes.unicode_minus'] = False

# # # 数据准备
# # data = {
# #     'sip_dv': 174.725008,
# #     'Impl-BE': 82.100000,
# #     'Platform': 44.972252,
# #     'DFX': 18.848747,
# #     'Impl-FE': 13.196243,
# #     'SoCDV & SYSIPDV': 10.979816,
# #     'Processor': 9.511786,
# #     'Cluster': 7.922340,
# #     'APP & SIP_Design': 7.809966,
# #     'DCE IPDV': 7.023351,
# #     'SysDV & CommonIPDV': 5.618681,
# #     'mc ipdv': 4.707633,
# #     'interconnect': 4.378348,
# #     'Impl-Analog': 4.315733,
# #     'SIPI': 3.236800,
# #     'SocPV': 2.596276,
# #     'IMPL_IP_Dev': 1.404670,
# #     'SOCDE': 1.404670,
# #     'IP_fabri': 0.000000,
# #     'NPE&IP_amos': 0.000000,
# #     'package': 0.000000
# # }

# # # 按值排序
# # sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
# # teams = list(sorted_data.keys())
# # values = list(sorted_data.values())

# # # 创建图表
# # fig, ax = plt.subplots(figsize=(12, 8))

# # # 绘制柱状图
# # bars = ax.bar(teams, values, color='royalblue')

# # # 添加数值标签
# # for bar in bars:
# #     height = bar.get_height()
# #     ax.text(bar.get_x() + bar.get_width()/2., height,
# #             f'{height:.2f}',
# #             ha='center', va='bottom', color='black')

# # # 设置图表标题和标签
# # ax.set_title('2025年2-5月各团队本地机器账单总费用排名', fontsize=14)
# # ax.set_xlabel('团队名称', fontsize=12)
# # ax.set_ylabel('费用(万元)', fontsize=12)

# # # 旋转x轴标签
# # plt.xticks(rotation=45, ha='right')

# # # 设置网格线
# # ax.set_axisbelow(True)
# # ax.grid(True, axis='y', linestyle='--', alpha=1.0)

# # # 添加水印
# # plt.figtext(
# #     0.9, 0.02,
# #     'Enflame A plan',
# #     ha='right',
# #     fontsize=10,
# #     color='gray',
# #     alpha=0.7,
# #     style='italic'
# # )

# # # 调整布局
# # plt.tight_layout()

# # # 保存图片
# # plt.savefig('output/2025_2-5月团队本地机器账单排名.png', dpi=300, bbox_inches='tight')
# # plt.savefig('output/2025_2-5月团队本地机器账单排名.svg', format='svg', bbox_inches='tight')

# # image_path = '.\\output/pic.png'
# # if os.name == 'nt':  # Windows
# #     os.startfile(image_path)


# # print("已成功绘制图像")
