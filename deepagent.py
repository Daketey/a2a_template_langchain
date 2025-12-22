import os
import asyncio
from deepagents import create_deep_agent, CompiledSubAgent
from langchain.agents import create_agent
from agent import agent1, agent2
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

top_model = ChatOpenAI(model="gpt-4o-mini", openai_api_key=os.getenv("OPENAI_API_KEY"))


# --------------------------
# Wrap existing LangChain agent as a subagent
# --------------------------
solver_subagent = CompiledSubAgent(
    name="solver-agent",
    description="Solves math problems using MCP tools, but needs validation of results",
    runnable=agent1  # your existing MCP-enabled agent
)

reviewer_subagent = CompiledSubAgent(
    name="reviewer-agent",
    description="Validates and extends solver-agent outputs",
    runnable=agent2
)

subagents = [solver_subagent, reviewer_subagent]

# --------------------------
# Create main DeepAgent
# --------------------------
deep_agent = create_deep_agent(
    model=top_model,  # Main model for top-level reasoning
    system_prompt="You are a coordinator agent. Assign tasks to subagents and combine their results.",
    subagents=subagents,
)

# --------------------------
# Run DeepAgent
# --------------------------
async def main():
    print("\n🚀 Starting DeepAgents Workflow with Subagents")
    print("=" * 60)

    messages = [HumanMessage(content="Add 3 and 5, then multiply by 12")]

    result = await deep_agent.ainvoke(
        {
            "messages": messages,
            "max_iterations": 3  # prevent infinite loops
        }
    )

    print("\n🧠 Final Output")
    print("=" * 60)
    print(result["messages"][-1].content)
    print("\n✅ Workflow Completed")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
