# SQL AI 分析工具

一个使用 LLM 进行 SQL 分析的工具，AI应用开发的初始项目

# 1. 环境安装

```powershell
# 官网下载 python.org 安装包，安装时勾选 "Add to PATH"
python --version        # 确认 3.12+

# 安装 uv（Rust 编写的现代 Python 包管理器，比 pip 快 10 倍+）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 新打开一个 powershell 窗口
uv --version
```

依赖安装

```
uv add openai fastapi uvicorn pydantic pytest httpx python-dotenv
```

```
```

# 2. 测试
```sh
# samples/explain_01.txt 放一份真实 EXPLAIN 输出（EXPLAIN 后复制结果）
uv run python main.py \
  --sql "SELECT * FROM orders WHERE user_id = 123 AND status = 'PAID' ORDER BY created_at DESC" \
  --explain-file samples/explain_01.txt

# 流式调试模式
uv run python main.py --sql "..." --explain-file samples/explain_01.txt --stream
```
