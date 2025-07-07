#!/usr/bin/env python3
"""
Simple web server to test Discord MCP Server
Uses a simpler approach to avoid asyncio issues
"""

import os
import time
import threading
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import discord
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Global variables
discord_client = None
discord_ready = False
discord_loop = None

class SimpleDiscordClient:
    """Simple Discord client for web testing"""
    
    def __init__(self):
        self.bot_token = os.getenv("DISCORD_BOT_TOKEN")
        if not self.bot_token:
            raise ValueError("DISCORD_BOT_TOKEN is required")
        
        # Initialize Discord client
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        
        # Setup events
        @self.client.event
        async def on_ready():
            global discord_ready
            print(f"✅ Discord client ready: {self.client.user}")
            discord_ready = True
        
        self.loop = None
    
    async def start_client(self):
        """Start the Discord client"""
        await self.client.start(self.bot_token)
    
    def run_client(self):
        """Run Discord client in thread"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.start_client())

# Initialize Discord client
discord_client = SimpleDiscordClient()

def start_discord_thread():
    """Start Discord client in background thread"""
    discord_thread = threading.Thread(target=discord_client.run_client, daemon=True)
    discord_thread.start()
    return discord_thread

# Helper functions that run in the Discord thread
def run_in_discord_loop(coro):
    """Run a coroutine in the Discord client's event loop"""
    if not discord_client.loop:
        raise RuntimeError("Discord client not started")
    
    future = asyncio.run_coroutine_threadsafe(coro, discord_client.loop)
    return future.result(timeout=30)

async def find_channel(channel_identifier: str):
    """Find a Discord channel by name or ID"""
    if not discord_client.client.is_ready():
        return None
    
    # Remove # if present
    channel_name = channel_identifier.lstrip('#')
    
    # Try to find by ID first
    if channel_name.isdigit():
        channel = discord_client.client.get_channel(int(channel_name))
        if channel:
            return channel
    
    # Try to find by name
    for guild in discord_client.client.guilds:
        for channel in guild.text_channels:
            if channel.name.lower() == channel_name.lower():
                return channel
    
    return None

async def send_message_async(channel: str, message: str):
    """Send a message to a Discord channel"""
    try:
        target_channel = await find_channel(channel)
        if not target_channel:
            return {"success": False, "content": f"❌ Channel '{channel}' not found"}
        
        sent_message = await target_channel.send(message)
        return {
            "success": True, 
            "content": f"✅ Message sent to #{target_channel.name} (ID: {sent_message.id})"
        }
        
    except Exception as e:
        return {"success": False, "content": f"❌ Error sending message: {str(e)}"}

async def get_messages_async(channel: str, limit: int = 10):
    """Get recent messages from a Discord channel"""
    try:
        if limit > 50:
            limit = 50
        
        target_channel = await find_channel(channel)
        if not target_channel:
            return {"success": False, "content": f"❌ Channel '{channel}' not found"}
        
        messages = []
        async for message in target_channel.history(limit=limit):
            messages.append(f"👤 {message.author.name}: {message.content}")
        
        if not messages:
            return {"success": True, "content": f"📭 No messages found in #{target_channel.name}"}
        
        result = f"📋 Last {len(messages)} messages from #{target_channel.name}:\n\n"
        result += "\n".join(reversed(messages))
        return {"success": True, "content": result}
        
    except Exception as e:
        return {"success": False, "content": f"❌ Error getting messages: {str(e)}"}

async def get_channel_info_async(channel: str):
    """Get information about a Discord channel"""
    try:
        target_channel = await find_channel(channel)
        if not target_channel:
            return {"success": False, "content": f"❌ Channel '{channel}' not found"}
        
        info = f"📊 Channel Information for #{target_channel.name}\n\n"
        info += f"🆔 Channel ID: {target_channel.id}\n"
        info += f"📂 Channel Type: {target_channel.type}\n"
        info += f"🏠 Server: {target_channel.guild.name}\n"
        info += f"📅 Created: {target_channel.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        if hasattr(target_channel, 'topic') and target_channel.topic:
            info += f"📝 Topic: {target_channel.topic}\n"
        
        if hasattr(target_channel, 'category') and target_channel.category:
            info += f"📁 Category: {target_channel.category.name}\n"
        
        return {"success": True, "content": info}
        
    except Exception as e:
        return {"success": False, "content": f"❌ Error getting channel info: {str(e)}"}

# Web routes
@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('.', 'web_test.html')

@app.route('/status')
def status():
    """Check connection status"""
    return jsonify({
        "discord_ready": discord_ready,
        "bot_user": str(discord_client.client.user) if discord_ready else None,
        "guild_count": len(discord_client.client.guilds) if discord_ready else 0
    })

@app.route('/mcp-tool', methods=['POST'])
def mcp_tool():
    """Handle MCP tool calls"""
    if not discord_ready:
        return jsonify({
            "success": False,
            "content": "❌ Discord client not ready. Please wait..."
        }), 503
    
    data = request.json
    tool_name = data.get('tool')
    arguments = data.get('arguments', {})
    
    try:
        if tool_name == 'send_message':
            result = run_in_discord_loop(
                send_message_async(
                    arguments.get('channel', ''),
                    arguments.get('message', '')
                )
            )
        elif tool_name == 'get_messages':
            result = run_in_discord_loop(
                get_messages_async(
                    arguments.get('channel', ''),
                    arguments.get('limit', 10)
                )
            )
        elif tool_name == 'get_channel_info':
            result = run_in_discord_loop(
                get_channel_info_async(
                    arguments.get('channel', '')
                )
            )
        else:
            result = {
                "success": False,
                "content": f"❌ Unknown tool: {tool_name}"
            }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "content": f"❌ Error: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Simple Discord MCP Web Tester...")
    print("📱 Open http://localhost:5000 in your browser")
    print("⏳ Waiting for Discord client to connect...")
    
    # Start Discord client
    start_discord_thread()
    
    # Wait for Discord to be ready
    while not discord_ready:
        time.sleep(1)
    
    print("✅ Discord client ready! Starting web server...")
    app.run(debug=True, host='0.0.0.0', port=5000) 