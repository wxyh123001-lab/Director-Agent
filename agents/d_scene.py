import json
import os
import anthropic
from state import DirectorState
from agents.utils import parse_json_response

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """你是一位专业的场景设计师。根据故事分析结果，设计每个场景的具体环境细节。
严格以 JSON 格式返回，不要有任何额外文字。
返回格式：
{
  "scenes": [
    {
      "scene_id": 1,
      "location": "地点名称",
      "background": "背景环境描述（具体可视化）",
      "time": "时间（清晨/正午/黄昏/深夜等）",
      "weather": "天气与气氛描述",
      "lighting": "光线特征",
      "props": ["关键道具1", "关键道具2"]
    }
  ]
}
场景数量与剧本场景数量保持一致（3-5个）。"""

def scene_node(state: DirectorState) -> dict:
    story = state["story"]
    user_prompt = f"""
原始描述：{state["user_input"]}
故事类型：{story.get("story_type")}
情感基调：{story.get("tone")}
核心冲突：{story.get("conflict")}

请据此设计3-5个具体场景的环境细节。
"""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    text = response.content[0].text.strip()
    scenes = parse_json_response(text)
    return {"scenes": scenes}
