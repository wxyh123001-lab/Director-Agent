import pytest
from unittest.mock import patch, MagicMock
from state import DirectorState
from agents.b_story import story_node

def make_mock_response(content: str):
    msg = MagicMock()
    msg.content = [MagicMock(text=content)]
    return msg

@patch("agents.b_story.client")
def test_story_node_returns_story_dict(mock_client):
    mock_client.messages.create.return_value = make_mock_response(
        '{"story_type": "爱情", "tone": "温馨", "conflict": "身份差距", "perspective": "第三人称"}'
    )
    state: DirectorState = {
        "user_input": "一个赛博朋克爱情故事",
        "story": {}, "script": {}, "scenes": {}, "style": {}, "output": {}
    }
    result = story_node(state)
    assert "story" in result
    assert result["story"]["story_type"] == "爱情"
    assert result["story"]["tone"] == "温馨"
    assert result["story"]["conflict"] == "身份差距"
    assert result["story"]["perspective"] == "第三人称"
