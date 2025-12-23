import asyncio
from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from agent import agent1, agent2
from langchain_core.callbacks import BaseCallbackHandler

# ----------------------------
# Tool callback (silent but traceable)
# ----------------------------
class ToolCallback(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        tool_name = serialized.get("name", "unknown")
        print(f"    🔧 Tool started → {tool_name}")

tool_callback = ToolCallback()

# ----------------------------
# Shared State (Conversation)
# ----------------------------
class AgentState(TypedDict):
    messages: List[Dict[str, str]]

# ----------------------------
# Agent Nodes
# ----------------------------
async def agent1_node(state: AgentState):
    response = await agent1.ainvoke(
        {"messages": state["messages"]},
        config={"callbacks": [tool_callback]}
    )

    reply = str(response["messages"][-1].content)
    state["messages"].append({"role": "assistant", "content": reply})
    return state


async def agent2_node(state: AgentState):
    response = await agent2.ainvoke(
        {"messages": state["messages"]},
        config={"callbacks": [tool_callback]}
    )

    reply = str(response["messages"][-1].content)
    state["messages"].append({"role": "assistant", "content": reply})
    return state

# ----------------------------
# Build Graph
# ----------------------------
graph = StateGraph(AgentState)

graph.add_node("agent1", agent1_node)
graph.add_node("agent2", agent2_node)

graph.set_entry_point("agent1")
graph.add_edge("agent1", "agent2")
graph.add_edge("agent2", END)

app = graph.compile()

# ----------------------------
# Interactive Loop
# ----------------------------
async def main():
    print("\n🤖 Multi-Agent Conversational System")
    print("Type 'exit' to quit")
    print("=" * 60)

    state: AgentState = {"messages": []}

    while True:
        user_input = input("\n🧑 User: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("\n👋 Conversation ended")
            break

        # Append new user turn
        state["messages"].append({
            "role": "user",
            "content": user_input
        })

        # Run one conversational turn
        state = await app.ainvoke(state)

        # Print only the latest assistant reply
        print("\n🤖 Assistant:")
        print(state["messages"][-1]["content"])
        print("-" * 60)

if __name__ == "__main__":
    asyncio.run(main())
