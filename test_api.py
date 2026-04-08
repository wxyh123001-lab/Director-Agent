"""
运行前：把下面的 YOUR_KEY_HERE 换成你的真实 Anthropic API Key
运行方式：python test_api.py
"""
import os
import sys

# ===== 在这里填入你的 API Key =====
API_KEY = "YOUR_KEY_HERE"
# ===================================

os.environ["ANTHROPIC_API_KEY"] = API_KEY

print("Step 1: 检查 key 格式...")
if not API_KEY.startswith("sk-ant-"):
    print(f"  警告：key 格式看起来不对（应以 sk-ant- 开头），当前：{API_KEY[:10]}...")
else:
    print(f"  OK: {API_KEY[:12]}...")

print("\nStep 2: 测试 Anthropic API 连通性...")
try:
    import anthropic
    client = anthropic.Anthropic(api_key=API_KEY)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=20,
        messages=[{"role": "user", "content": "Reply with: OK"}],
    )
    print(f"  API 响应: {response.content[0].text}")
    print("  API 连通成功！")
except Exception as e:
    print(f"  API 连接失败: {e}")
    sys.exit(1)

print("\nStep 3: 测试完整 pipeline（B agent 单步）...")
try:
    from agents.b_story import story_node
    from state import DirectorState

    state: DirectorState = {
        "user_input": "一个赛博朋克世界里的爱情故事",
        "story": {}, "script": {}, "scenes": {}, "style": {}, "output": {}
    }
    result = story_node(state)
    print(f"  故事类型: {result['story'].get('story_type')}")
    print(f"  情感基调: {result['story'].get('tone')}")
    print("  B agent OK！")
except Exception as e:
    print(f"  B agent 失败: {e}")
    sys.exit(1)

print("\n所有测试通过！可以运行完整 pipeline：")
print("  python main.py \"一个赛博朋克世界里的爱情故事\"")
