import os
import json
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain_core.tools import tool
from src.config import LLM_MODEL, DEEPSEEK_API_KEY, DEEPSEEK_API_BASE

class CodeAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL, 
            openai_api_key=DEEPSEEK_API_KEY,
            openai_api_base=DEEPSEEK_API_BASE,
            temperature=0
        )

    def analyze(self, description: str, repo_path: str) -> str:
        """
        手动实现 ReAct 循环，确保 Agent 必须调用工具。
        """
        print(f"  [Agent] 启动专家级代码审计 Agent...")

        @tool
        def list_files(path: str = ".", max_depth: int = 3) -> str:
            """树状展示目录结构。支持 max_depth 参数（默认 3），能帮你一眼看清深层 Java/Python 项目结构。"""
            target = os.path.join(repo_path, path)
            if not os.path.exists(target):
                return f"错误：路径 {path} 不存在。"
            
            output = [f"目录 {path} 的树状结构 (深度上限 {max_depth})："]
            
            def walk_dir(current_dir, current_rel, depth):
                if depth > max_depth: return
                try:
                    items = sorted(os.listdir(current_dir))
                    for item in items:
                        if item.startswith('.'): continue
                        item_full = os.path.join(current_dir, item)
                        item_rel = os.path.join(current_rel, item)
                        indent = "  " * (depth + 1)
                        if os.path.isdir(item_full):
                            output.append(f"{indent}📁 {item}/")
                            walk_dir(item_full, item_rel, depth + 1)
                        else:
                            output.append(f"{indent}📄 {item}")
                except:
                    pass

            walk_dir(target, path, 0)
            result = "\n".join(output)
            if len(result) > 10000:
                result = result[:10000] + "\n... (结构过长，建议分目录查看)"
            return result

        @tool
        def search_code(query: str) -> str:
            """全局搜索包含指定关键词的内容（不区分大小写）。这能帮你瞬间定位到核心逻辑所在的具体文件。"""
            matches = []
            print(f"    > 正在全局检索关键词: '{query}'...")
            for root, dirs, files in os.walk(repo_path):
                if any(p.startswith('.') for p in root.split(os.sep)): continue
                for file in files:
                    if file.lower().endswith(('.py', '.java', '.js', '.c', '.cpp', '.h', '.go', 'makefile', '.html', '.md', '.json', '.xml')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                for i, line in enumerate(f, 1):
                                    if query.lower() in line.lower():
                                        rel_path = os.path.relpath(file_path, repo_path)
                                        matches.append(f"📄 {rel_path} (行 {i}): {line.strip()[:100]}")
                                        if len(matches) > 30: break
                        except: pass
                    if len(matches) > 30: break
                if len(matches) > 30: break
            
            if not matches:
                return f"未找到包含 '{query}' 的代码内容。"
            return "搜索结果 (前 30 条):\n" + "\n".join(matches)

        @tool
        def read_file(file_path: str) -> str:
            """读取指定文件的源代码内容。参数 file_path 为相对于代码库根目录的路径。"""
            full_path = os.path.join(repo_path, file_path)
            if not os.path.exists(full_path):
                return f"错误：文件 {file_path} 不存在。"
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    return content[:25000] # 扩大读取量
            except Exception as e:
                return f"读取文件失败: {e}"

        # 显式绑定工具
        tools_dict = {"list_files": list_files, "read_file": read_file, "search_code": search_code}
        llm_with_tools = self.llm.bind_tools([list_files, read_file, search_code])
        
        system_prompt = (
            "你是一个顶级的代码诊断专家。你目前处于隔离环境，必须通过工具感知代码。\n"
            "【最高效策略】：\n"
            "1. **全局视野**: 首先调用 `list_files` 获取根目录及其子目录的树状结构，快速定位项目模块。\n"
            "2. **精准制导**: 使用 `search_code` 搜索描述中的关键类名、函数名或文本。这比逐层点开目录快得多！\n"
            "3. **深入分析**: 定位嫌疑点后，用 `read_file` 严谨分析逻辑，杜绝猜测。\n"
            "4. **专业报告**: 你的目标是产出包含原因、证据、修改建议的诊断报告。严禁直接打印原始工具输出。"
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"【问题单描述】：{description}\n请开始调查。")
        ]

        print(f"  [Agent] 正在进行自主推理探测 (Max 10 步)...")
        
        for i in range(10):
            response = llm_with_tools.invoke(messages)
            messages.append(response)
            
            if not response.tool_calls:
                break
            
            for tool_call in response.tool_calls:
                tool_func = tools_dict.get(tool_call["name"])
                print(f"    > 正在调用工具: {tool_call['name']}({tool_call['args']})")
                tool_result = tool_func.invoke(tool_call["args"])
                print(f"    > 工具返回数据完成")
                messages.append(ToolMessage(content=tool_result, tool_call_id=tool_call["id"]))
        
        print(f"  [完成] 专家探测结束。")
        return messages[-1].content
