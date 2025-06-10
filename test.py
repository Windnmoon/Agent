import matplotlib.pyplot as plt
import matplotlib as mpl  # 新增全局设置模块
import os


# --- 关键修复步骤 ---
# 1. 设置全局中文字体（微软雅黑）
mpl.rcParams['font.family'] = 'Microsoft YaHei'  # Windows系统字体[6,7](@ref)
mpl.rcParams['axes.unicode_minus'] = False  # 修复负号显示问题[1,2](@ref)



# # 数据准备
# months = ['2025年2月', '2025年3月', '2025年4月', '2025年5月']
# amounts = [12.8282, 12.8282, 12.8282, 12.8282]

# # 创建图表
# fig, ax = plt.subplots(figsize=(8, 6))

# # 绘制柱状图
# bars = ax.bar(months, amounts, color='royalblue')

# # 3. 添加数据标签（使用备用字体）
# for bar in bars:
#     height = bar.get_height()
#     ax.text(bar.get_x() + bar.get_width()/2., height,
#             f'{height:.2f}',  # 保留两位小数
#             ha='center', va='bottom')  # 显式应用字体[7](@ref)

# # 4. 设置中文标签（双保险）
# ax.set_xlabel('月份')  # X轴标签
# ax.set_ylabel('金额（万元）')  # Y轴标签
# ax.set_title('2025年季度数据')  # 标题

# plt.tight_layout()
# plt.show()





# 数据准备
months = ['2025年2月', '2025年3月', '2025年4月', '2025年5月']
amounts = [12.8282, 12.8282, 12.8282, 12.8282]
# 设置样式
# plt.style.use('seaborn-v0_8-whitegrid')

# 创建图表

fig, ax = plt.subplots(figsize=(8, 6))


# 绘制柱状图
bars = ax.bar(months, amounts, color='royalblue')
# 添加数据标签
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}',
            ha='center', va='bottom')
# 设置标题和标签
ax.set_title('DFX团队2025年2月至5月磁盘账单金额',  pad=20)
ax.set_xlabel('月份')
ax.set_ylabel('金额（万元）')
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

# plt.grid(axis='y', alpha=0.5, linestyle='-')

ax.set_axisbelow(True)
ax.grid(True, axis='y', linestyle='--', alpha=1.0)

plt.show()
print("已成功绘制图像")
