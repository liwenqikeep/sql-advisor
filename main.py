import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv          # uv add python-dotenv
from llm_client import LLMClient
from prompts import SYSTEM_PROMPT, build_user_content
from models import SqlAnalysis

def main():
    parser = argparse.ArgumentParser(description="慢 SQL 分析助手")
    parser.add_argument("--sql", required=True)
    parser.add_argument("--explain-file", required=True, help="EXPLAIN 输出文件")
    parser.add_argument("--stream", action="store_true", help="流式输出原始回复")
    args = parser.parse_args()

    load_dotenv()                       # 从 .env 读 API Key
    client = LLMClient(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )

    explain_text = Path(args.explain_file).read_text(encoding="utf-8")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_content(args.sql, explain_text)},
    ]

    if args.stream:                     # 调试模式：看原始流式输出
        for chunk in client.stream(messages):
            print(chunk, end="", flush=True)
        return

    analysis = client.chat_json(messages, SqlAnalysis)      # 结构化输出
    print(f"\n📌 总结: {analysis.summary}")
    print(f"⚠️  问题: {', '.join(analysis.problems)}")
    for i, s in enumerate(analysis.suggestions, 1):
        print(f"{i}. [{s.impact}] {s.action}\n   依据: {s.reason}")

if __name__ == "__main__":
    main()