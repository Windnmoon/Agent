from langchain_experimental.utilities import PythonREPL


code1 = '''import matplotlib.pyplot as plt
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

code2 = '''print("心想事成")'''
print("大吉大利")

ans = PythonREPL().run(code1)
print(ans)
print("吉星高照")
