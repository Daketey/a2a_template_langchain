import asyncio
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from agent import agent1, agent2
from langchain_core.callbacks import BaseCallbackHandler

# ----------------------------
# Callback to debug tool usage
# ----------------------------
class ToolCallback(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        tool_name = serialized.get("name", "unknown")
        print(f"    🔧 Tool started → {tool_name}")

tool_callback = ToolCallback()

# -------- Shared State --------
class AgentState(TypedDict):
    question: str
    responses: List[Dict[str, Any]]

# -------- LangGraph Nodes --------
async def agent1_node(state: AgentState):
    user_query = state["question"]

    print("\n🧠 AGENT 1")
    print("─" * 60)
    print(f"📥 Question:\n  {user_query}")
    print("─" * 60)

    response = await agent1.ainvoke(
        {"messages": [{"role": "user", "content": user_query}]},
        config={"callbacks": [tool_callback]}
    )

    output = str(response["messages"][-1].content)
    state["responses"].append({"agent1": output})

    print(f"\n📤 Agent 1 Response:\n  {output}")
    print("\n➡️  Passing output to Agent 2")
    print("=" * 60)

    return state

async def agent2_node(state: AgentState):
    user_query = state["question"]
    previous_response = state["responses"]

    prompt = (
        f"User Asked:\n{user_query}\n\n"
        f"Agents Responded:\n{previous_response}\n\n"
        "Analyze the answer or provide additional calculations using tools."
    )

    print("\n🧠 AGENT 2")
    print("─" * 60)
    print(f"📥 Context Prompt:\n{prompt}")
    print("─" * 60)

    response = await agent2.ainvoke(
        {"messages": [{"role": "user", "content": prompt}]},
        config={"callbacks": [tool_callback]}
    )

    output = str(response["messages"][-1].content)
    state["responses"].append({"agent2": output})

    print(f"\n📤 Agent 2 Final Response:\n  {output}")
    print("=" * 60)

    return state

# -------- Build Graph --------
graph = StateGraph(AgentState)

graph.add_node("agent1", agent1_node)
graph.add_node("agent2", agent2_node)

graph.set_entry_point("agent1")
graph.add_edge("agent1", "agent2")
graph.add_edge("agent2", END)

app = graph.compile()

# -------- Runner --------
async def main():
    print("\n🚀 Starting Agent-to-Agent (A2A) Workflow")
    print("=" * 60)

    initial_state = {
        "question": "Add 3 and 5, then multiply by 12",
        "responses": []
    }

    await app.ainvoke(initial_state)

    print("\n✅ Workflow completed")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
