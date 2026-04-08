import json
from unittest.mock import patch, MagicMock
from state import DirectorState
from agents.d_scene import scene_node

def make_mock_response(content: str):
    msg = MagicMock()
    msg.content = [MagicMock(text=content)]
    return msg

@patch("agents.d_scene.client")
def test_scene_node_returns_scenes_dict(mock_client):
    mock_response = {
        "scenes": [
            {
                "scene_id": 1,
                "location": "霓虹街头",
                "background": "密集的高楼大厦，全息广告牌闪烁",
                "time": "深夜",
                "weather": "小雨，湿漉漉的路面反光",
                "lighting": "冷蓝色霓虹光",
                "props": ["旧摩托车", "破损的全息地图"]
            }
        ]
    }
    mock_client.messages.create.return_value = make_mock_response(json.dumps(mock_response))
    state: DirectorState = {
        "user_input": "赛博朋克爱情故事",
        "story": {"story_type": "爱情", "tone": "温馨", "conflict": "身份差距", "perspective": "第三人称"},
        "script": {}, "scenes": {}, "style": {}, "output": {}
    }
    result = scene_node(state)
    assert "scenes" in result
    assert len(result["scenes"]["scenes"]) == 1
    assert result["scenes"]["scenes"][0]["location"] == "霓虹街头"
    assert result["scenes"]["scenes"][0]["time"] == "深夜"
