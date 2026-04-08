import pytest
from unittest.mock import patch, MagicMock
from state import DirectorState
from agents.c_script import script_node

def make_mock_response(content: str):
    msg = MagicMock()
    msg.content = [MagicMock(text=content)]
    return msg

@patch("agents.c_script.client")
def test_script_node_returns_script_dict(mock_client):
    mock_response = {
        "characters": [
            {
                "name": "陈明",
                "background": "底层黑客",
                "appearance": "瘦高，眼神锐利",
                "costume": "破旧皮夹克，全息护目镜",
                "state": "疲惫但坚定"
            }
        ],
        "scenes": [
            {
                "scene_id": 1,
                "title": "初遇",
                "characters": ["陈明"],
                "dialogue": [{"speaker": "陈明", "line": "你就是他们说的那个人？"}],
                "action": "陈明从阴影中走出，扫视四周"
            }
        ]
    }
    import json
    mock_client.messages.create.return_value = make_mock_response(json.dumps(mock_response))
    state: DirectorState = {
        "user_input": "赛博朋克爱情故事",
        "story": {"story_type": "爱情", "tone": "温馨", "conflict": "身份差距", "perspective": "第三人称"},
        "script": {}, "scenes": {}, "style": {}, "output": {}
    }
    result = script_node(state)
    assert "script" in result
    assert len(result["script"]["characters"]) == 1
    assert result["script"]["characters"][0]["name"] == "陈明"
    assert result["script"]["characters"][0]["costume"] == "破旧皮夹克，全息护目镜"
    assert len(result["script"]["scenes"]) == 1
