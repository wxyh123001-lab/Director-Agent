import json
import os
import anthropic
from state import DirectorState
from agents.utils import parse_json_response

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """你是一位专业的故事分析师。
根据用户的描述，识别故事的核心要素，并严格以 JSON 格式返回，不要有任何额外文字。
返回格式：
{
  "story_type": "故事类型（爱情/科幻/悬疑/动作/剧情等）",
  "tone": "情感基调（温馨/紧张/压抑/欢快/史诗等）",
  "conflict": "核心冲突描述（一句话）",
  "perspective": "叙事视角（第一人称/第三人称/多视角）"
}"""

def story_node(state: DirectorState) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": state["user_input"]}],
    )
    text = response.content[0].text.strip()
    story = parse_json_response(text)
    return {"story": story}
