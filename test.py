import pandas as pd

# 读取Excel文件
file_path = './data/HSE资源费用统计总表_202504.xlsx'
sheet_name = '费用统计'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 筛选SoCDV & SYSIPDV团队的数据
team_name = 'SoCDV & SYSIPDV'
team_data = df[df.iloc[:,2] == team_name]
print(team_data)
print(team_data.iloc[1, 3])

# 提取所需列的数据
disk_bill = team_data.iloc[0, 3]  # 磁盘账单(列3)
local_machine_bill = team_data.iloc[0, 4]  # 本地机器账单(列4)
total_bill = team_data.iloc[0, 6]  # 合计账单(列6)

# 创建结果DataFrame
result = pd.DataFrame({
    '团队名称': [team_name],
    '磁盘账单': [disk_bill],
    '本地机器账单': [local_machine_bill],
    '合计账单': [total_bill]
})

# 保存到csv文件
output_path = './output/SoCDV_SYSIPDV_bills.csv'
result.to_csv(output_path, index=False, encoding='utf-8-sig')

# 打印结果
print(f"提取结果已保存到: {output_path}")
print("\n提取的数据如下:")
print(f"团队名称: {team_name}")
print(f"磁盘账单: {disk_bill}")
print(f"本地机器账单: {local_machine_bill}")
print(f"合计账单: {total_bill}")