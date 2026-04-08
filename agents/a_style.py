import json
from state import DirectorState
from agents.utils import parse_json_response
from agents.client import chat

SYSTEM_PROMPT = """你是一位专业的导演和摄影指导。根据完整的剧本和场景设计，推荐具体的拍摄风格。
严格以 JSON 格式返回。
返回格式：
{
  "global_style": "整体拍摄风格定性（一句话）",
  "scenes": [
    {
      "scene_id": 1,
      "camera": "镜头语言建议（景别+运镜方式）",
      "editing_technique": "剪辑手法（转场方式+节奏控制）",
      "filter_style": "推荐滤镜和色调风格（具体描述）"
    }
  ]
}"""

def style_node(state: DirectorState) -> dict:
    script = state["script"]
    scenes = state["scenes"]
    user_prompt = f"""故事基调：{state["story"].get("tone")}
角色列表：{json.dumps([c["name"] for c in script.get("characters", [])], ensure_ascii=False)}
场景列表：{json.dumps(scenes.get("scenes", []), ensure_ascii=False)}
剧本场景：{json.dumps(script.get("scenes", []), ensure_ascii=False)}
请据此为每个场景推荐拍摄风格、剪辑手法和滤镜色调。"""
    text = chat(SYSTEM_PROMPT, user_prompt, max_tokens=2048)
    return {"style": parse_json_response(text)}
