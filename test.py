import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import xlwings as xw

# 设置中文字体
mpl.rcParams['font.family'] = 'Microsoft YaHei'
mpl.rcParams['axes.unicode_minus'] = False

# 准备数据
months = ['2月', '3月', '4月', '5月']
front_end = [1144, 1024, 1051, 940]
middle_end = [351, 236, 209, 255]
back_end = [20, 16, 16, 16]

# 创建图表
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制折线图
ax.plot(months, front_end, label='前端集群', marker='o', color='#09469B')
ax.plot(months, middle_end, label='中端集群', marker='s', color='#FF7F0E')
ax.plot(months, back_end, label='后端集群', marker='^', color='#2CA02C')

# 添加数据标签
for x, y in zip(months, front_end):
    ax.text(x, y, f'{y}', ha='center', va='bottom', color='black')
for x, y in zip(months, middle_end):
    ax.text(x, y, f'{y}', ha='center', va='bottom', color='black')
for x, y in zip(months, back_end):
    ax.text(x, y, f'{y}', ha='center', va='bottom', color='black')

# 设置图表元素
ax.set_title('2025年2-5月集群节点数变化', pad=20)
ax.set_xlabel('月份')
ax.set_ylabel('节点数(台)')
ax.legend()

# 添加网格线
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

# 确保output文件夹存在
os.makedirs('output', exist_ok=True)

# 保存图像
plt.savefig('.\\output\\cluster_nodes_trend.png', dpi=300, bbox_inches='tight')
plt.savefig('.\\output\\cluster_nodes_trend.svg', format='svg', bbox_inches='tight')
os.startfile('.\\output\\cluster_nodes_trend.png')

# 输出表格
wb = xw.Book()
sheet = wb.sheets[0]

# 写入表头
sheet.range('A1').value = '月份'
sheet.range('B1').value = '前端集群(台)'
sheet.range('C1').value = '中端集群(台)'
sheet.range('D1').value = '后端集群(台)'

# 写入数据
for i, month in enumerate(months):
    sheet.range(f'A{i+2}').value = f'2025年{month}'
    sheet.range(f'B{i+2}').value = front_end[i]
    sheet.range(f'C{i+2}').value = middle_end[i]
    sheet.range(f'D{i+2}').value = back_end[i]

# 保存表格
wb.save('.\\output\\cluster_nodes_data.xlsx')
wb.close()

print("已成功绘制图像")
print("已成功输出表格")