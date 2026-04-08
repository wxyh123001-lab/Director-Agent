from typing import TypedDict


class DirectorState(TypedDict):
    """全局状态定义

    属性：
        user_input: 用户原始描述
        story: B agent 输出
        script: C agent 输出（人物、服装、状态、剧本）
        scenes: D agent 输出（场景、环境）
        style: A agent 输出（拍摄风格）
        output: E agent 最终输出
    """
    user_input: str
    search: dict   # Search Agent 输出，USE_SEARCH=false 时为 {}
    story: dict
    script: dict
    scenes: dict
    style: dict
    output: dict
