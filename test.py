import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置中文字体
mpl.rcParams['font.family'] = 'Microsoft YaHei'
mpl.rcParams['axes.unicode_minus'] = False

# 准备数据
months = ['2月', '3月', '4月', '5月']
weeks = ['Week1', 'Week2', 'Week3', 'Week4', 'Week5']
data = {
    '2月': [0.254, 0.254, 0.229, 0.197, 0.238],
    '3月': [0.38, 0.197, 0.38, 0.254, 0.321],  # Week5数据缺失
    '4月': [0.246, 0.38, 0.448, 0.38, 0.412],  # Week5数据缺失
    '5月': [0.254, 0.254, 0.229, 0.197, 0.234]  # Week5数据缺失
}

# 创建图形
fig, ax = plt.subplots(figsize=(12, 6))

# 设置柱状图位置
x = range(len(weeks))
width = 0.2  # 柱状图宽度

# 绘制每个月的柱状图
for i, month in enumerate(months):
    values = data[month]
    positions = [pos + i * width for pos in x]
    bars = ax.bar(positions, values, width, label=month, color='royalblue')
    
    # 添加数据标签
    for bar in bars:
        height = bar.get_height()
        if height > 0:  # 只显示有效数据
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom')

# 设置图表标题和标签
ax.set_title('SOCDE团队2025年2-5月slot利用率周统计')
ax.set_xlabel('周数')
ax.set_ylabel('slot利用率')
ax.set_xticks([pos + 1.5 * width for pos in x])
ax.set_xticklabels(weeks)
ax.set_ylim(0, 0.5)

# 添加图例
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

# 保存图像
plt.savefig('output/SOCDE_slot_utilization.png', dpi=300, bbox_inches='tight')
plt.savefig('output/SOCDE_slot_utilization.svg', format='svg', bbox_inches='tight')

plt.close()
print("已成功绘制图像")

