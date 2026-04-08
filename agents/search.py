# agents/search.py
import os
from tavily import TavilyClient
from state import DirectorState


def search_node(state: DirectorState) -> dict:
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    results = client.search(state["user_input"], max_results=5)
    summary = "\n\n".join([r["content"] for r in results["results"] if r.get("content")])
    return {"search": {"results": summary}}
