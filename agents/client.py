# agents/client.py
import os
from openai import OpenAI

def get_client() -> OpenAI:
    return OpenAI(
        api_key=os.environ.get("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

MODEL = "qwen-plus"

def chat(system: str, user: str, max_tokens: int = 2048) -> str:
    """统一调用入口，强制 JSON 输出，自动重试最多 3 次。"""
    client = get_client()
    for attempt in range(3):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
            max_tokens=max_tokens,
        )
        text = response.choices[0].message.content.strip()
        if text:
            return text
    raise RuntimeError("模型连续 3 次返回空内容")
