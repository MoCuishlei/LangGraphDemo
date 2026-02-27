from typing import TypedDict, List, Dict, Annotated
from langgraph.graph import StateGraph, END
from src.nodes.parser import parse_excel_tickets
from src.nodes.downloader import clone_or_update_repo
from src.nodes.analyzer import CodeAnalyzer
from src.nodes.reporter import generate_report

# 定义 Agent 状态
class AgentState(TypedDict):
    excel_path: str
    tickets: List[Dict]
    analysis_results: List[Dict]

def excel_loader_node(state: AgentState):
    print("--- 步骤 1 & 2: 解析与筛选 Excel ---")
    tickets = parse_excel_tickets(state["excel_path"])
    return {"tickets": tickets}

def analyzer_node(state: AgentState):
    print("\n--- 步骤 3 & 4: 代码下载与智能分析 ---")
    analyzer = CodeAnalyzer()
    results = []
    
    total = len(state["tickets"])
    for idx, ticket in enumerate(state["tickets"], 1):
        git_url = ticket["git_url"]
        desc = ticket["description"]
        
        print(f"\n[任务 {idx}/{total}] 正在处理: {desc[:50]}...")
        
        # 下载/检查代码
        local_path = clone_or_update_repo(git_url)
        
        # 分析代码
        if local_path:
            analysis = analyzer.analyze(desc, local_path)
        else:
            analysis = "Failed to clone repository."
        
        ticket["analysis"] = analysis
        results.append(ticket)
        
    return {"analysis_results": results}

def reporter_node(state: AgentState):
    print("--- 步骤 5: 生成报告 ---")
    report_path = generate_report(state["analysis_results"])
    return {"report_path": report_path}

# 构建图
workflow = StateGraph(AgentState)

workflow.add_node("loader", excel_loader_node)
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("reporter", reporter_node)

workflow.set_entry_point("loader")
workflow.add_edge("loader", "analyzer")
workflow.add_edge("analyzer", "reporter")
workflow.add_edge("reporter", END)

app = workflow.compile()
