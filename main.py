import os
import sys
from dotenv import load_dotenv

# 必须在 import graph/agents 之前加载，否则 client 创建时拿不到 key
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from graph import build_graph
from state import DirectorState

def run(user_input: str):
    if not os.environ.get("DASHSCOPE_API_KEY"):
        print("Error: DASHSCOPE_API_KEY 未设置，请检查 .env 文件")
        sys.exit(1)

    print(f"\n开始处理：{user_input}\n")
    graph = build_graph()

    initial_state: DirectorState = {
        "user_input": user_input,
        "search": {},
        "story": {},
        "script": {},
        "scenes": {},
        "style": {},
        "output": {},
    }

    result = graph.invoke(initial_state)
    output = result["output"]
    print("\n生成完成！文件保存路径：")
    print(f"  JSON : {output['json_path']}")
    print(f"  MD   : {output['md_path']}")
    print(f"  DOCX : {output['docx_path']}")
    return result

if __name__ == "__main__":
    user_input = sys.argv[1] if len(sys.argv) > 1 else "一个赛博朋克世界里的爱情故事"
    run(user_input)
