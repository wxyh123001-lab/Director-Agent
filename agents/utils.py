import re
import json


def parse_json_response(text: str) -> dict:
    """解析 Claude 返回的 JSON，兼容 markdown 代码块包裹的情况。

    支持以下格式：
    - 纯 JSON: {"key": "value"}
    - markdown fence: ```json {"key": "value"} ```
    - 无语言标记的 fence: ``` {"key": "value"} ```

    Args:
        text: Claude 返回的文本

    Returns:
        解析后的 dict 对象

    Raises:
        json.JSONDecodeError: 如果 JSON 解析失败
    """
    text = text.strip()

    # 移除 markdown 代码块标记
    # 先移除开头的 ```json 或 ```
    text = re.sub(r"^```(?:json)?\s*", "", text)
    # 再移除末尾的 ```
    text = re.sub(r"\s*```$", "", text)

    # 修剪空白符后再解析
    text = text.strip()

    # strict=False 允许 JSON 字符串中包含未转义的控制字符（模型有时会输出）
    return json.loads(text, strict=False)
