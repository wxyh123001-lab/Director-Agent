import os
import sys
from graph import build_graph
from state import DirectorState

def run(user_input: str):
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY 环境变量未设置")
        sys.exit(1)

    print(f"\n开始处理：{user_input}\n")
    graph = build_graph()

    initial_state: DirectorState = {
        "user_input": user_input,
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
