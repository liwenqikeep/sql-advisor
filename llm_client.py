import json
import re
import sys
import time
from typing import Iterator
from openai import OpenAI
from pydantic import BaseModel

class LLMClient:
    def __init__(self, api_key: str, base_url: str, model: str = "deepseek-chat"):
        self._client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def chat(self, messages: list[dict], temperature: float = 0.2,
             response_format: dict | None = None) -> str:
        """带指数退避重试的同步调用"""
        for attempt in range(3):
            try:
                resp = self._client.chat.completions.create(
                    model=self.model, messages=messages, temperature=temperature,
                    response_format=response_format,
                )
                return resp.choices[0].message.content
            except Exception as e:
                if attempt == 2:
                    raise
                time.sleep(2 ** attempt)        # 1s, 2s, 4s 退避

    def stream(self, messages: list[dict]) -> Iterator[str]:
        """流式输出，逐段 yield"""
        stream = self._client.chat.completions.create(
            model=self.model, messages=messages, stream=True
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    @staticmethod
    def _extract_json(text: str) -> str:
        """剥离 Markdown 代码块 / 前后杂文，提取纯 JSON"""
        text = text.strip()
        fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
        if fence:
            return fence.group(1).strip()
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            return text[start:end + 1]
        return text

    def chat_json(self, messages: list[dict], schema: type[BaseModel]):
        """结构化输出：让模型输出严格符合 Pydantic 模型的 JSON"""
        messages = messages + [{
            "role": "system",
            "content": (
                "只输出一个 JSON 对象：不要 markdown 代码块，不要解释文字。"
                f"字段结构要求：{json.dumps(schema.model_json_schema(), ensure_ascii=False)}"
            ),
        }]
        last_err: Exception | None = None
        for attempt in range(3):
            raw = self.chat(messages, temperature=0,
                            response_format={"type": "json_object"})
            try:
                return schema.model_validate_json(self._extract_json(raw))
            except Exception as e:
                last_err = e
                print(f"[chat_json] 第 {attempt + 1} 次解析失败: {e}", file=sys.stderr)
                print(f"[chat_json] 模型原始输出:\n{raw[:800]}", file=sys.stderr)
                messages.append({"role": "assistant", "content": raw})
                messages.append({"role": "user", "content": "JSON 格式错误，请严格按要求重新输出，不要任何其他文字"})
        raise ValueError(f"模型 3 次均未输出合法 JSON，最后错误: {last_err}")
