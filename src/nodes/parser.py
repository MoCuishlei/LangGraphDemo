import pandas as pd
import re
import os
from typing import List, Dict

def parse_excel_tickets(file_path: str) -> List[Dict]:
    """
    解析 Excel 问题单，筛选备注中包含 Git 地址的行。
    预期 Excel 格式：包含 '问题描述' 和 '备注' 列。
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return []

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return []

    # 简单的 Git 地址正则匹配
    git_pattern = r'https?://[^\s/$.?#].[^\s]*\.git'

    valid_tickets = []
    
    # 假设列名为 '备注' 和 '描述'
    # 如果用户没有提供具体列名，这里可以做更通用的映射
    remark_col = next((c for c in df.columns if '备注' in c), None)
    desc_col = next((c for c in df.columns if '描述' in c or '问题单' in c), None)

    if not remark_col:
        print("Warning: Could not find '备注' column.")
        return []

    for _, row in df.iterrows():
        remark = str(row[remark_col])
        git_urls = re.findall(git_pattern, remark)
        
        if git_urls:
            valid_tickets.append({
                "description": str(row[desc_col]) if desc_col else "No description",
                "git_url": git_urls[0],  # 取第一个匹配到的 git 地址
                "original_remark": remark
            })

    return valid_tickets

if __name__ == "__main__":
    # 测试代码
    data = parse_excel_tickets("data/test_tickets.xlsx")
    print(f"Parsed {len(data)} valid tickets.")
    for t in data:
        print(t)
