import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
df = pd.read_csv('./output/DFX_team_bills_summary.csv')

# 设置样式
plt.style.use('seaborn-v0_8-whitegrid')

# 创建图表
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制柱状图
bars = ax.bar(
    df['Unnamed: 0'], 
    df['合计账单（万元）'], 
    color='royalblue'
)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2., 
        height, 
        f'{height:.2f}', 
        ha='center', 
        va='bottom'
    )

# 设置标题和标签
ax.set_title('Monthly Bill Summary', fontsize=14)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Total Bill (10k yuan)', fontsize=12)

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
plt.savefig('output/monthly_bill_summary.png', dpi=300, bbox_inches='tight')
plt.savefig('output/monthly_bill_summary.svg', format='svg', bbox_inches='tight')

print("已成功绘制图像")