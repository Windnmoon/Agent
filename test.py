import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib import font_manager
import matplotlib as mpl

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'Noto Sans CJK SC']
plt.rcParams['axes.unicode_minus'] = False

# 读取前10产品数据
file_path = 'data/2023年8月-9月销售记录.xlsx'
df = pd.read_excel(file_path)

# 计算每个产品的销售额
df['销售额'] = df['单价(元)'] * df['销售量']

# 按产品名称分组并计算总销售额
sales_by_product = df.groupby('产品名')['销售额'].sum().reset_index()

# 按销售额降序排序
sales_by_product = sales_by_product.sort_values('销售额', ascending=False)

# 获取销售额排名前10的产品
top_10_products = sales_by_product.head(10)

# 获取这些产品的单价信息
top_10_with_price = pd.merge(
    top_10_products, 
    df[['产品名', '单价(元)']].drop_duplicates(), 
    on='产品名'
)

# 创建一个高质量的图表
plt.figure(figsize=(14, 8))

# 设置背景样式
plt.style.use('seaborn-v0_8-whitegrid')

# 定义一个优雅的渐变配色方案
colors = ['#4361EE', '#3F37C9', '#4895EF', '#4CC9F0', '#560BAD', 
          '#7209B7', '#B5179E', '#F72585', '#F25C54', '#F4845F']

# 创建柱状图
bars = plt.bar(
    range(len(top_10_with_price)), 
    top_10_with_price['销售额'],
    color=colors,
    width=0.7,
    edgecolor='white',
    linewidth=1.5
)

# 添加产品名称作为x轴标签
plt.xticks(
    range(len(top_10_with_price)),
    top_10_with_price['产品名'],
    rotation=45,
    ha='right',
    fontsize=12
)

# 在每个柱子上方添加销售额数值
for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2.,
        height + 5000,  # 稍微偏移以便清晰显示
        f'{int(height):,}',
        ha='center',
        va='bottom',
        fontsize=11,
        fontweight='bold',
        color=colors[i]
    )

# 设置图表标题和轴标签（英文）
plt.title('Top 10 Products by Sales', fontsize=20, fontweight='bold', pad=20)
plt.xlabel('Product Name', fontsize=14, labelpad=15)
plt.ylabel('Sales (CNY)', fontsize=14, labelpad=15)

# 调整y轴范围，确保数值标签有足够空间
plt.ylim(0, top_10_with_price['销售额'].max() * 1.15)

# 添加网格线以提高可读性
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 添加Manus水印
plt.figtext(
    0.9, 0.02, 
    'Powered by Manus', 
    ha='right', 
    fontsize=10, 
    color='gray', 
    alpha=0.7,
    style='italic'
)

# 美化图表边框
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_linewidth(0.5)
plt.gca().spines['bottom'].set_linewidth(0.5)

# 添加轻微的阴影效果增强立体感
for bar in bars:
    bar.set_zorder(1)
    bar_color = bar.get_facecolor()
    plt.gca().add_patch(
        plt.Rectangle(
            (bar.get_x(), 0), 
            bar.get_width(), 
            bar.get_height(),
            fill=True,
            facecolor=bar_color,
            alpha=0.1,
            zorder=0,
            transform=plt.gca().transData,
            linewidth=0
        )
    )

# 调整布局
plt.tight_layout()

# 保存图表
plt.savefig('data/top_10_products_sales_english.png', dpi=300, bbox_inches='tight')
plt.savefig('data/top_10_products_sales_english.svg', format='svg', bbox_inches='tight')

print("英文标签图表已保存为 top_10_products_sales_english.png 和 top_10_products_sales_english.svg")

