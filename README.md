# LangGraph 缺陷诊断 Agent

本项目是一个基于 LangGraph 的自动化工具，旨在通过解析 Excel 格式的问题单，自动定位并分析代码库中的缺陷。

## 主要功能

1.  **Excel 解析**：自动提取包含 Git 仓库地址的问题单。
2.  **代码自动化克隆**：根据备注中的地址自动下载或更新相关源码。
3.  **智能缺陷分析**：利用 LLM 结合问题描述和源代码，指出代码中可能存在的问题点。
4.  **报告生成**：将所有分析结果汇总生成易于阅读的 Markdown 报告。

## 快速开始

### 1. 环境准备

安装依赖：
```bash
pip install -r requirements.txt
```

配置环境变量 `.env`（注意：由于安全原因，`.env` 文件已被 `.gitignore` 忽略，不会上传至 GitHub。请在本地项目根目录手动创建 `.env` 文件，并参考以下格式填入你的配置）：
```env
DEEPSEEK_API_KEY=your_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com
LLM_MODEL=deepseek-chat
```

### 2. 使用方法

1. 将包含问题单的 Excel 文件命名为 `tickets.xlsx` 并放入 `data/` 目录。
   - Excel 需包含“描述”和“备注”字样的列。
   - “备注”列中需包含 `.git` 结尾的 Git 地址。
2. 运行程序：
```bash
python main.py
```
3. 查看生成的 `report.md` 报告。

## 项目结构

- `src/nodes/`: 各个 Agent 执行阶段的逻辑实现。
- `src/graph.py`: LangGraph 工作流定义。
- `main.py`: 程序入口。
- `repos/`: 下载的代码库存储位置。
