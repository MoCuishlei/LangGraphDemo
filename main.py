from src.graph import app
import os
import sys

def main():
    # 检查环境变量
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("Error: DEEPSEEK_API_KEY environment variable not set.")
        # sys.exit(1)

    # 输入 Excel 路径，默认使用 data/tickets.xlsx
    excel_path = "data/tickets.xlsx"
    if not os.path.exists(excel_path):
        print(f"Excel file not found at {excel_path}. Please place your problem tickets Excel there.")
        return

    # 初始化状态
    initial_state = {
        "excel_path": excel_path,
        "tickets": [],
        "analysis_results": []
    }

    print("\n" + "="*50)
    print("🚀 缺陷诊断 Agent 启动中...")
    print("="*50)

    try:
        # 使用 stream 模式展示步骤详情（LangGraph 支持查看流转过程）
        for output in app.stream(initial_state):
            for node_name, node_output in output.items():
                print(f"\n✅ [节点完成: {node_name}]")
        
        print("\n" + "="*50)
        print("🎉 所有工作流执行完毕！")
        print(f"📊 最终报告已生成: report.md")
        print("="*50)
    except Exception as e:
        print(f"\n❌ 执行过程中发生错误: {e}")

if __name__ == "__main__":
    main()
