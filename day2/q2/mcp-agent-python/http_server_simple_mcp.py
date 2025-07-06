#!/usr/bin/env python3
"""
HTTP Bridge with Proper MCP Tool Pattern
This shows the CORRECT way to think about MCP tools
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# Import our tool functions
from tools.create_meeting import create_meeting
from tools.find_optimal_slots import find_optimal_slots
from tools.detect_scheduling_conflicts import detect_scheduling_conflicts

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🎓 LEARNING: MCP Tool Registry Pattern
class MCPToolRegistry:
    """This simulates how MCP manages tools"""
    
    def __init__(self):
        self.tools = {}
    # Use register_tool() to store your tool in a generic way inside your own registry (MCP-style).
    def register_tool(self, name: str, description: str, parameters: dict, func):
        """Register an MCP tool (like @mcp.tool() decorator)"""
        self.tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "func": func
        }
        print(f"🔧 [MCP Registry] Registered tool: {name}")
    

    # ✅ Use get_openai_tools() to convert your internal tool into OpenAI’s JSON format (function calling).
    # 🔁 Converts MCP tool format → OpenAI function calling JSON format
    def get_openai_tools(self):
        print("get_openai_tools",self)
        """Convert MCP tools to OpenAI format"""
        openai_tools = []
        for tool_name, tool_info in self.tools.items():
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_info["description"],
                    "parameters": tool_info["parameters"]
                }
            }
            openai_tools.append(openai_tool)
        return openai_tools
    
    def execute_tool(self, tool_name: str, tool_args: dict):
        """Execute MCP tool by name (automatic dispatch)"""
        if tool_name in self.tools:
            tool_func = self.tools[tool_name]["func"]
            print(f"🔧 [MCP] Auto-executing tool: {tool_name}")
            result = tool_func(**tool_args)
            print(f"🔧 [MCP] Tool result: {result}")
            return result
        else:
            raise ValueError(f"Tool {tool_name} not found in MCP registry")

# 🎓 LEARNING: Create MCP tool registry
mcp_registry = MCPToolRegistry()

# 🎓 LEARNING: Register tools (like @mcp.tool() decorator)
mcp_registry.register_tool(
    name="create_meeting_tool",
    description="Create a new meeting with specified participants and time",
    parameters={
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Title of the meeting"},
            "participants": {"type": "array", "items": {"type": "string"}, "description": "List of participant names"},
            "duration": {"type": "integer", "description": "Duration in minutes"},
            "start_time": {"type": "string", "description": "Start time in ISO format"}
        },
        "required": ["title", "participants", "duration", "start_time"]
    },
    func=create_meeting  # Direct function reference
)

# Register find_optimal_slots tool
mcp_registry.register_tool(
    name="find_optimal_slots_tool",
    description="Find optimal meeting slots for participants with AI-powered recommendations",
    parameters={
        "type": "object",
        "properties": {
            "participants": {"type": "array", "items": {"type": "string"}, "description": "List of participant names"},
            "duration": {"type": "integer", "description": "Meeting duration in minutes"},
            "date_range": {"type": "string", "description": "Date range in format 'YYYY-MM-DD to YYYY-MM-DD'"}
        },
        "required": ["participants", "duration", "date_range"]
    },
    func=find_optimal_slots
)

# Register detect_scheduling_conflicts tool
mcp_registry.register_tool(
    name="detect_scheduling_conflicts_tool",
    description="Detect scheduling conflicts for a user within a specific time range",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "User ID or name to check conflicts for"},
            "time_range": {"type": "string", "description": "Time range in format 'YYYY-MM-DDTHH:MM to YYYY-MM-DDTHH:MM'"}
        },
        "required": ["user_id", "time_range"]
    },
    func=detect_scheduling_conflicts
)

@app.route('/', methods=['GET'])
def health_check():
    """Health check with MCP tool info"""
    return jsonify({
        "status": "running",
        "server": "MCP HTTP Bridge (Simple MCP Pattern)",
        "registered_tools": list(mcp_registry.tools.keys())
    })

@app.route('/chat', methods=['POST'])
def handle_chat():
    """
    🎓 LEARNING: HTTP endpoint using proper MCP tool pattern
    """
    try:
        # Step 1: Get query
        data = request.get_json()
        user_query = data.get('query')
        
        print(f"🔵 [HTTP Bridge] Received query: {user_query}")
        
        if not user_query:
            return jsonify({"error": "No query provided"}), 400
        
        # Step 2: Get tools from MCP registry (automatic discovery)
        available_tools = mcp_registry.get_openai_tools()
        print("available_tools",available_tools)
        print(f"🔵 [MCP] Available tools: {[t['function']['name'] for t in available_tools]}")
        
        # Step 3: Create conversation
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful meeting assistant. Use the available MCP tools to help users."
            },
            {
                "role": "user", 
                "content": user_query
            }
        ]
        
        # Step 4: Call OpenAI with MCP tools
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=available_tools,
            tool_choice="auto"
        )
        
        # Step 5: Execute MCP tools automatically
        if response.choices[0].message.tool_calls:
            print(f"🔵 [MCP] AI wants to use tools!")
            
            for tool_call in response.choices[0].message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 [MCP] Tool call: {tool_name}")
                print(f"🔧 [MCP] Arguments: {tool_args}")
                
                # 🎓 LEARNING: Automatic MCP tool execution (no if statements!)
                tool_result = mcp_registry.execute_tool(tool_name, tool_args)
                
                # Add to conversation
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tool_call]
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result)
                })
            
            # Get final response
            final_response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            
            return jsonify({"response": final_response.choices[0].message.content})
        
        else:
            return jsonify({"response": response.choices[0].message.content})
            
    except Exception as e:
        print(f"🔴 [HTTP Bridge] Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting HTTP Bridge with MCP Tool Pattern...")
    print("🔗 This demonstrates proper MCP tool management!")
    print(f"🔧 Registered MCP tools: {list(mcp_registry.tools.keys())}")
    app.run(host='0.0.0.0', port=5001, debug=True) 