#!/usr/bin/env python3
"""
HTTP Bridge for MCP Tools
This file creates an HTTP server that Node.js can call,
and internally uses our MCP tools to process queries.
Manula tool calling here!!
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# Import our MCP tool
from tools.create_meeting import create_meeting

# Load environment variables
load_dotenv()

# Create Flask app (HTTP server)
app = Flask(__name__)
CORS(app)  # Allow Node.js to call this server

# Initialize OpenAI client
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# 🎓 LEARNING: This is where we define what tools the AI can use
available_tools = [
    {
        "type": "function",
        "function": {
            "name": "create_meeting",
            "description": "Create a new meeting with specified participants and time",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the meeting"},
                    "participants": {"type": "array", "items": {"type": "string"}, "description": "List of participant names"},
                    "duration": {"type": "integer", "description": "Duration in minutes"},
                    "start_time": {"type": "string", "description": "Start time in ISO format (e.g., '2024-12-10T09:00:00')"}
                },
                "required": ["title", "participants", "duration", "start_time"]
            }
        }
    }
]

@app.route('/', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "running",
        "server": "MCP HTTP Bridge",
        "available_tools": ["create_meeting"]
    })

@app.route('/chat', methods=['POST'])
def handle_chat():
    """
    🎓 LEARNING: This is the main endpoint that Node.js calls
    
    Flow:
    1. Receive user query from Node.js
    2. Send query to OpenAI with available tools
    3. If AI wants to use tools, call them
    4. Return response to Node.js
    """
    try:
        # Step 1: Get the user query from Node.js
        data = request.get_json()
        user_query = data.get('query')
        
        print(f"🔵 [HTTP Bridge] Received query at http_server.py: {user_query}")
        
        if not user_query:
            return jsonify({"error": "No query provided"}), 400
        
        # Step 2: Create conversation with OpenAI
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful meeting assistant. Use the available tools to help users manage their meetings."
            },
            {
                "role": "user", 
                "content": user_query
            }
        ]
        
        print(f"🔵 [HTTP Bridge] Sending to OpenAI with {len(available_tools)} tools")
        
        # Step 3: Call OpenAI with available tools
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=available_tools,
            tool_choice="auto"
        )
        
        # Step 4: Check if AI wants to use tools
        if response.choices[0].message.tool_calls:
            print(f"🔵 [HTTP Bridge] AI wants to use tools!",response.choices[0].message.tool_calls)
            
            # Process each tool call
            for tool_call in response.choices[0].message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                print(f"🔵 [HTTP Bridge] Calling tool: {tool_name}")
                print(f"🔵 [HTTP Bridge] Tool arguments: {tool_args}")
                
                # 🎓 LEARNING: This is where we call our MCP tool
                if tool_name == "create_meeting":
                    tool_result = create_meeting(
                        title=tool_args["title"],
                        participants=tool_args["participants"],
                        duration=tool_args["duration"],
                        start_time=tool_args["start_time"]
                    )
                    print(f"🔵 [HTTP Bridge] Tool result: {tool_result}")
                    
                    # Add tool result to conversation
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [tool_call]
                    })
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })
            
            # Get final response from AI
            final_response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            
            final_answer = final_response.choices[0].message.content
            print(f"🔵 [HTTP Bridge] Final response: {final_answer}")
            
            return jsonify({"response": final_answer})
        
        else:
            # AI didn't need to use tools
            simple_response = response.choices[0].message.content
            print(f"🔵 [HTTP Bridge] Simple response: {simple_response}")
            return jsonify({"response": simple_response})
            
    except Exception as e:
        print(f"🔴 [HTTP Bridge] Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting HTTP Bridge Server...")
    print("🔗 Node.js can now call: http://localhost:5000/chat")
    print("🔧 Available tools: create_meeting")
    app.run(host='0.0.0.0', port=5000, debug=True) 