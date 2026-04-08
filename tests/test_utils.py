import pytest
import json
from agents.utils import parse_json_response


class TestParseJsonResponse:
    """Test the parse_json_response utility function."""

    def test_parse_plain_json(self):
        """Test parsing plain JSON without markdown fence."""
        text = '{"key": "value"}'
        result = parse_json_response(text)
        assert result["key"] == "value"

    def test_parse_json_with_markdown_fence_json_lang(self):
        """Test parsing JSON with ```json fence."""
        text = '```json\n{"key": "value"}\n```'
        result = parse_json_response(text)
        assert result["key"] == "value"

    def test_parse_json_with_plain_fence(self):
        """Test parsing JSON with plain ``` fence."""
        text = '```\n{"key": "value"}\n```'
        result = parse_json_response(text)
        assert result["key"] == "value"

    def test_parse_complex_json_with_fence(self):
        """Test parsing complex nested JSON with markdown fence."""
        text = '''```json
{
  "name": "test",
  "values": [1, 2, 3],
  "nested": {
    "inner_key": "inner_value"
  }
}
```'''
        result = parse_json_response(text)
        assert result["name"] == "test"
        assert result["values"] == [1, 2, 3]
        assert result["nested"]["inner_key"] == "inner_value"

    def test_parse_json_with_extra_whitespace(self):
        """Test parsing JSON with extra whitespace around fence."""
        text = '  ```json  \n  {"key": "value"}  \n  ```  '
        result = parse_json_response(text)
        assert result["key"] == "value"

    def test_parse_json_array(self):
        """Test parsing JSON array at top level."""
        text = '```json\n[{"id": 1}, {"id": 2}]\n```'
        result = parse_json_response(text)
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1

    def test_parse_json_with_newlines(self):
        """Test parsing properly formatted JSON with newlines."""
        text = '''```json
{
  "story_type": "科幻",
  "tone": "紧张",
  "conflict": "人与机器的对抗",
  "perspective": "第一人称"
}
```'''
        result = parse_json_response(text)
        assert result["story_type"] == "科幻"
        assert result["tone"] == "紧张"
        assert result["conflict"] == "人与机器的对抗"

    def test_parse_json_chinese_chars(self):
        """Test parsing JSON with Chinese characters."""
        text = '```json\n{"名字": "测试", "数值": 42}\n```'
        result = parse_json_response(text)
        assert result["名字"] == "测试"
        assert result["数值"] == 42

    def test_parse_json_with_unicode_escape(self):
        """Test parsing JSON with unicode escape sequences."""
        text = '{"emoji": "\\ud83d\\ude00"}'
        result = parse_json_response(text)
        assert "emoji" in result

    def test_invalid_json_raises_error(self):
        """Test that invalid JSON raises JSONDecodeError."""
        text = '{"invalid": json}'
        with pytest.raises(json.JSONDecodeError):
            parse_json_response(text)

    def test_invalid_json_in_fence_raises_error(self):
        """Test that invalid JSON in fence raises JSONDecodeError."""
        text = '```json\n{"invalid": json}\n```'
        with pytest.raises(json.JSONDecodeError):
            parse_json_response(text)

    def test_empty_object(self):
        """Test parsing empty JSON object."""
        text = '{}'
        result = parse_json_response(text)
        assert result == {}

    def test_empty_object_with_fence(self):
        """Test parsing empty JSON object with fence."""
        text = '```json\n{}\n```'
        result = parse_json_response(text)
        assert result == {}
