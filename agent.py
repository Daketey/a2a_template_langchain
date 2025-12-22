import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

async def build_agents():
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": ["./mcp_server.py"],
            }
        }
    )

    tools = await client.get_tools()

    # ---- split tools by name ----
    add_tools = [t for t in tools if t.name == "add"]

    model = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)

    # only pass the add tool to agent1
    agent1 = create_agent(
        model=model,
        tools=add_tools,
        system_prompt="Use the available tools to answer user math questions step by step."
    )
    
    # pass both tools to agent2
    agent2 = create_agent(
        model=model,
        tools=tools,
        system_prompt="Use the available tools to verify and finalize user math questions step by step."
    )

    return agent1, agent2

agent1, agent2 = asyncio.run(build_agents())