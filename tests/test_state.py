from state import DirectorState

def test_state_has_required_keys():
    state: DirectorState = {
        "user_input": "一个赛博朋克爱情故事",
        "story": {},
        "script": {},
        "scenes": {},
        "style": {},
        "output": {},
    }
    assert state["user_input"] == "一个赛博朋克爱情故事"
    assert isinstance(state["story"], dict)
    assert isinstance(state["script"], dict)
    assert isinstance(state["scenes"], dict)
    assert isinstance(state["style"], dict)
    assert isinstance(state["output"], dict)
