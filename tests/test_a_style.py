import json
from unittest.mock import patch, MagicMock
from state import DirectorState
from agents.a_style import style_node

def make_mock_response(content: str):
    msg = MagicMock()
    msg.content = [MagicMock(text=content)]
    return msg

@patch("agents.a_style.client")
def test_style_node_returns_style_dict(mock_client):
    mock_response = {
        "global_style": "赛博朋克新黑色电影风格",
        "scenes": [
            {
                "scene_id": 1,
                "camera": "低角度仰拍，缓慢推进镜头",
                "editing_technique": "慢切，配合雨声节奏",
                "filter_style": "冷蓝青色调，高对比度，轻微颗粒感"
            }
        ]
    }
    mock_client.messages.create.return_value = make_mock_response(json.dumps(mock_response))
    state: DirectorState = {
        "user_input": "赛博朋克爱情故事",
        "story": {"story_type": "爱情", "tone": "温馨", "conflict": "身份差距", "perspective": "第三人称"},
        "script": {"characters": [], "scenes": [{"scene_id": 1}]},
        "scenes": {"scenes": [{"scene_id": 1, "location": "霓虹街头"}]},
        "style": {}, "output": {}
    }
    result = style_node(state)
    assert "style" in result
    assert result["style"]["global_style"] == "赛博朋克新黑色电影风格"
    assert len(result["style"]["scenes"]) == 1
    assert "editing_technique" in result["style"]["scenes"][0]
    assert "filter_style" in result["style"]["scenes"][0]
