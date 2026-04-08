# graph.py
from langgraph.graph import StateGraph, START, END
from state import DirectorState
from agents.b_story import story_node
from agents.c_script import script_node
from agents.d_scene import scene_node
from agents.a_style import style_node
from agents.e_output import output_node

def build_graph():
    builder = StateGraph(DirectorState)

    builder.add_node("story", story_node)
    builder.add_node("script", script_node)
    builder.add_node("scene", scene_node)
    builder.add_node("style", style_node)
    builder.add_node("output", output_node)

    # B agent 先跑
    builder.add_edge(START, "story")

    # C 和 D 并行（都从 story 出发）
    builder.add_edge("story", "script")
    builder.add_edge("story", "scene")

    # C 和 D 完成后进入 A
    builder.add_edge("script", "style")
    builder.add_edge("scene", "style")

    # A 完成后进入 E
    builder.add_edge("style", "output")
    builder.add_edge("output", END)

    return builder.compile()
