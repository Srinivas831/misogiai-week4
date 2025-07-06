# ❌ agent.py — this was for MCPAgent, not FastMCP


# from mcp import MCPAgent
# from openai import OpenAI
# from tools.create_meeting import create_meeting_tool
# import os
# from dotenv import load_dotenv

# # ✅ Load environment variables from .env
# load_dotenv()

# # ✅ 1. Load your model (e.g., OpenAI)
# llm = OpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

# # ✅ 2. Register your tools
# tools = [create_meeting_tool]

# # ✅ 3. Create the agent with tools and model
# agent = MCPAgent(tools=tools, model=llm)

# # ✅ 4. Define a function to run the agent
# def run_agent(query: str) -> str:
#     print(f"🧠 Agent received query: {query}")
#     result = agent.run(query)
#     print(f"🤖 Agent response: {result}")
#     return result
