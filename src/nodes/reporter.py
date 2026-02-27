import os

def generate_report(results: list, output_path: str = "report.md"):
    """
    将分析结果整理成 Markdown 报告。
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 缺陷诊断分析报告\n\n")
        f.write("| 问题描述 | Git 地址 | 分析结果 |\n")
        f.write("| :--- | :--- | :--- |\n")
        
        for item in results:
            desc = item.get("description", "N/A").replace("\n", " ")
            url = item.get("git_url", "N/A")
            analysis = item.get("analysis", "No analysis performed.").replace("\n", "<br>")
            f.write(f"| {desc} | {url} | {analysis} |\n")
            
    print(f"Report generated at {output_path}")
    return output_path
