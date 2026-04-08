from state import DirectorState
from agents.utils import parse_json_response
from agents.client import chat

SYSTEM_PROMPT = """你是一位专业的故事分析师。
根据用户的描述，识别故事的核心要素，严格以 JSON 格式返回。
返回格式：
{
  "story_type": "故事类型（爱情/科幻/悬疑/动作/剧情等）",
  "tone": "情感基调（温馨/紧张/压抑/欢快/史诗等）",
  "conflict": "核心冲突描述（一句话）",
  "perspective": "叙事视角（第一人称/第三人称/多视角）"
}"""

def story_node(state: DirectorState) -> dict:
    text = chat(SYSTEM_PROMPT, state["user_input"], max_tokens=512)
    return {"story": parse_json_response(text)}
