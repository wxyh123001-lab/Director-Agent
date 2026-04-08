# graph.py
import os
from langgraph.graph import StateGraph, START, END
from state import DirectorState
from agents.search import search_node
from agents.b_story import story_node
from agents.c_script import script_node
from agents.d_scene import scene_node
from agents.a_style import style_node
from agents.e_output import output_node


def _route_start(state: DirectorState) -> str:
    if os.environ.get("USE_SEARCH", "false").lower() == "true":
        return "search"
    return "story"


def build_graph():
    builder = StateGraph(DirectorState)

    builder.add_node("search", search_node)
    builder.add_node("story", story_node)
    builder.add_node("script", script_node)
    builder.add_node("scene", scene_node)
    builder.add_node("style", style_node)
    builder.add_node("output", output_node)

    # 条件起点：有 USE_SEARCH=true 时先走 search，否则直接 story
    builder.add_conditional_edges(START, _route_start, {"search": "search", "story": "story"})
    builder.add_edge("search", "story")

    # C 和 D 并行
    builder.add_edge("story", "script")
    builder.add_edge("story", "scene")

    # 汇合后进入 A → E
    builder.add_edge("script", "style")
    builder.add_edge("scene", "style")
    builder.add_edge("style", "output")
    builder.add_edge("output", END)

    return builder.compile()
