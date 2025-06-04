import pandas as pd
import matplotlib.pyplot as plt

# 设置样式
plt.style.use('seaborn-v0_8-whitegrid')

# 读取CSV文件
df = pd.read_csv('./output/HSE_teams_local_machine_cost_sorted.csv')

# 确保列名正确
x_col = 'HSE团队名称'
y_col = '本地机器账单（万元）'

# 创建图形
plt.figure(figsize=(12, 6))

# 绘制柱状图
bars = plt.bar(df[x_col], df[y_col], color='royalblue')

# 添加数值标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}',
             ha='center', va='bottom')

# 设置标题和标签
plt.title('Local Machine Cost by HSE Team (Sorted)', fontsize=14)
plt.xlabel('HSE Team Name', fontsize=12)
plt.ylabel('Cost (10k yuan)', fontsize=12)

# 旋转x轴标签
plt.xticks(rotation=45, ha='right')

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
plt.savefig('output/HSE_teams_local_machine_cost_bar1.png', dpi=300, bbox_inches='tight')

plt.close()

print("已成功绘制图像")