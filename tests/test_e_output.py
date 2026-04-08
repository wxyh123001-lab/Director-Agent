import json
import os
import tempfile
from unittest.mock import patch
from state import DirectorState
from agents.e_output import output_node

MOCK_STATE: DirectorState = {
    "user_input": "赛博朋克爱情故事",
    "story": {"story_type": "爱情", "tone": "温馨", "conflict": "身份差距", "perspective": "第三人称"},
    "script": {
        "characters": [
            {"name": "陈明", "background": "底层黑客", "appearance": "瘦高",
             "costume": "破旧皮夹克", "state": "疲惫但坚定"}
        ],
        "scenes": [
            {"scene_id": 1, "title": "初遇", "characters": ["陈明"],
             "dialogue": [{"speaker": "陈明", "line": "你是谁？"}],
             "action": "陈明走近"}
        ]
    },
    "scenes": {
        "scenes": [
            {"scene_id": 1, "location": "霓虹街头", "background": "高楼大厦",
             "time": "深夜", "weather": "小雨", "lighting": "冷蓝色", "props": ["摩托车"]}
        ]
    },
    "style": {
        "global_style": "赛博朋克新黑色电影",
        "scenes": [
            {"scene_id": 1, "camera": "低角度仰拍",
             "editing_technique": "慢切", "filter_style": "冷蓝色调"}
        ]
    },
    "output": {}
}

def test_output_node_creates_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("agents.e_output.OUTPUT_BASE", tmpdir):
            result = output_node(MOCK_STATE)
    assert "output" in result
    assert "json_path" in result["output"]
    assert "md_path" in result["output"]
    assert "docx_path" in result["output"]

def test_output_json_structure():
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("agents.e_output.OUTPUT_BASE", tmpdir):
            result = output_node(MOCK_STATE)
        with open(result["output"]["json_path"], encoding="utf-8") as f:
            data = json.load(f)
    assert "characters" in data
    assert "scenes" in data
    assert "global_style_prompt" in data
    assert data["characters"][0]["name"] == "陈明"
    assert "editing_technique" in data["scenes"][0]
    assert "filter_style" in data["scenes"][0]
