import json
import os
import anthropic
from state import DirectorState
from agents.utils import parse_json_response

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """你是一位专业的编剧。根据故事分析结果，创作详细的人物设定和分场剧本。
严格以 JSON 格式返回，不要有任何额外文字。
返回格式：
{
  "characters": [
    {
      "name": "角色姓名",
      "background": "角色背景（一句话）",
      "appearance": "外貌特点",
      "costume": "服装描述（具体、可视化）",
      "state": "当前状态（情绪+身体状态）"
    }
  ],
  "scenes": [
    {
      "scene_id": 1,
      "title": "场景标题",
      "characters": ["出场角色名列表"],
      "dialogue": [
        {"speaker": "角色名", "line": "台词"}
      ],
      "action": "场景动作描述"
    }
  ]
}"""

def script_node(state: DirectorState) -> dict:
    story = state["story"]
    user_prompt = f"""
原始描述：{state["user_input"]}
故事类型：{story.get("story_type")}
情感基调：{story.get("tone")}
核心冲突：{story.get("conflict")}
叙事视角：{story.get("perspective")}

请据此创作人物设定和分场剧本（3-5个场景）。
"""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    text = response.content[0].text.strip()
    script = parse_json_response(text)
    return {"script": script}
