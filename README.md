# 哲学论文写作助手 · Philosophy Writing Lab

哲学论文写作辅助工具，帮助研究者：
- **📚 搜索文献**：根据主题查找相关哲学书籍和论文
- **🔍 漏洞检测**：分析论证中的逻辑谬误、缺失前提、概念模糊等问题
- **⚡ 反例生成**：生成思想实验、真实案例、边界情况三类反例
- **🔗 相关论证**：发现支持性、对立性和变体论证

## 技术栈

- 后端：Python FastAPI + Anthropic Claude API
- 前端：React + Vite
- 论文搜索：Semantic Scholar API（免费）

## 快速开始

### 1. 后端

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # 编辑 .env，填入 ANTHROPIC_API_KEY
uvicorn main:app --reload --port 8000
```

### 2. 前端

```bash
cd frontend
npm install
npm run dev  # 启动开发服务器，自动代理 /api 到后端
```

## 项目结构

```
philosophy-writing-lab/
├── backend/
│   ├── main.py              # FastAPI 入口 + 5 个 API 路由
│   ├── llm.py               # Claude API 封装（单网关模式）
│   ├── prompts.py           # 各功能的 System/User Prompt 模板
│   ├── config.py            # 配置（环境变量）
│   └── tools/               # 功能模块（Agent 的 tool-use 设计）
│       ├── paper_search.py  # 论文搜索（Semantic Scholar + LLM）
│       ├── book_search.py   # 哲学书籍推荐
│       ├── fallacy_check.py # 论证漏洞检测
│       ├── counterexample.py# 反例生成
│       └── related_args.py  # 相关论证检索
└── frontend/
    └── src/
        ├── App.jsx          # 主界面（输入 + Tab 切换）
        ├── index.css        # Dark Academia 主题
        └── components/      # 输入、结果展示组件
```
