from state import DirectorState
from agents.utils import parse_json_response
from agents.client import chat

SYSTEM_PROMPT = """你是一位专业的场景设计师。根据故事分析结果，设计每个场景的具体环境细节。
严格以 JSON 格式返回。
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
    user_prompt = f"""原始描述：{state["user_input"]}
故事类型：{story.get("story_type")}
情感基调：{story.get("tone")}
核心冲突：{story.get("conflict")}
请据此设计3-5个具体场景的环境细节。"""
    text = chat(SYSTEM_PROMPT, user_prompt, max_tokens=2048)
    return {"scenes": parse_json_response(text)}
