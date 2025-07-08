"""
Discord MCP Server - Proper MCP Implementation
This server uses stdio transport to connect with AI clients like Claude Desktop
"""

import asyncio
import json
import os
import sys
from typing import Optional, List, Dict, Any

import discord
from discord.ext import commands
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool, CallToolResult

# Load environment variables
load_dotenv()

class DiscordMCPServer:
    """Discord MCP Server with stdio transport"""
    
    def __init__(self):
        """Initialize the Discord MCP Server"""
        
        # Get Discord configuration
        self.bot_token = os.getenv("DISCORD_BOT_TOKEN")
        if not self.bot_token:
            raise ValueError("DISCORD_BOT_TOKEN is required in .env file or environment variables")
        
        # Initialize Discord client with proper intents
        intents = discord.Intents.default()
        intents.message_content = True  # Required for reading message content
        intents.guilds = True
        intents.guild_messages = True
        
        self.discord_client = discord.Client(intents=intents)
        
        # Create ready event
        self.discord_ready = asyncio.Event()
        
        # Setup Discord events
        @self.discord_client.event
        async def on_ready():
            print(f"✅ Discord client ready: {self.discord_client.user}")
            print(f"📊 Connected to {len(self.discord_client.guilds)} guilds")
            self.discord_ready.set()
        
        @self.discord_client.event
        async def on_error(event, *args, **kwargs):
            print(f"❌ Discord error in {event}: {args}")
        
        # MCP Server
        self.server = Server("discord-mcp-server")
        
        # Setup handlers
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup MCP request handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available Discord tools"""
            return [
                Tool(
                    name="send_message",
                    description="Send a message to a Discord channel",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel": {"type": "string", "description": "Channel name (without #) or channel ID"},
                            "message": {"type": "string", "description": "Message content to send"}
                        },
                        "required": ["channel", "message"]
                    }
                ),
                Tool(
                    name="get_messages",
                    description="Get recent messages from a Discord channel",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel": {"type": "string", "description": "Channel name (without #) or channel ID"},
                            "limit": {"type": "integer", "description": "Number of messages to retrieve (1-50, default: 10)", "default": 10, "minimum": 1, "maximum": 50}
                        },
                        "required": ["channel"]
                    }
                ),
                Tool(
                    name="get_channel_info",
                    description="Get information about a Discord channel",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel": {"type": "string", "description": "Channel name (without #) or channel ID"}
                        },
                        "required": ["channel"]
                    }
                ),
                Tool(
                    name="list_channels",
                    description="List all available channels in connected Discord servers",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "server_name": {"type": "string", "description": "Optional: filter by server name", "default": ""}
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls"""
            
            try:
                # Wait for Discord to be ready
                if not self.discord_ready.is_set():
                    await asyncio.wait_for(self.discord_ready.wait(), timeout=30.0)
                
                if name == "send_message":
                    result = await self.send_message(arguments["channel"], arguments["message"])
                elif name == "get_messages":
                    result = await self.get_messages(arguments["channel"], arguments.get("limit", 10))
                elif name == "get_channel_info":
                    result = await self.get_channel_info(arguments["channel"])
                elif name == "list_channels":
                    result = await self.list_channels(arguments.get("server_name", ""))
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                return CallToolResult(
                    content=[TextContent(type="text", text=result)]
                )
                
            except asyncio.TimeoutError:
                error_msg = "❌ Discord client not ready (timeout)"
                return CallToolResult(
                    content=[TextContent(type="text", text=error_msg)],
                    isError=True
                )
            except Exception as e:
                error_msg = f"❌ Error executing {name}: {str(e)}"
                return CallToolResult(
                    content=[TextContent(type="text", text=error_msg)],
                    isError=True
                )
    
    async def find_channel(self, channel_identifier: str) -> Optional[discord.TextChannel]:
        """Find a Discord channel by name or ID"""
        
        # Remove # if present
        channel_name = channel_identifier.lstrip('#')
        
        # Try to find by ID first
        if channel_name.isdigit():
            try:
                channel = self.discord_client.get_channel(int(channel_name))
                if channel and isinstance(channel, discord.TextChannel):
                    return channel
            except ValueError:
                pass
        
        # Try to find by name
        for guild in self.discord_client.guilds:
            for channel in guild.text_channels:
                if channel.name.lower() == channel_name.lower():
                    return channel
        
        return None
    
    async def send_message(self, channel: str, message: str) -> str:
        """Send a message to a Discord channel"""
        
        try:
            # Find the channel
            target_channel = await self.find_channel(channel)
            if not target_channel:
                available_channels = []
                for guild in self.discord_client.guilds:
                    for ch in guild.text_channels:
                        available_channels.append(f"#{ch.name}")
                
                result = f"❌ Channel '{channel}' not found.\n"
                result += f"Available channels: {', '.join(available_channels[:10])}"
                if len(available_channels) > 10:
                    result += f" and {len(available_channels) - 10} more..."
                return result
            
            # Check permissions
            if not target_channel.permissions_for(target_channel.guild.me).send_messages:
                return f"❌ No permission to send messages in #{target_channel.name}"
            
            # Send the message
            sent_message = await target_channel.send(message)
            return f"✅ Message sent to #{target_channel.name} in {target_channel.guild.name} (Message ID: {sent_message.id})"
            
        except discord.Forbidden:
            return f"❌ No permission to send messages in {channel}"
        except discord.HTTPException as e:
            return f"❌ Discord API error: {str(e)}"
        except Exception as e:
            return f"❌ Error sending message: {str(e)}"
    
    async def get_messages(self, channel: str, limit: int = 10) -> str:
        """Get recent messages from a Discord channel"""
        
        try:
            # Validate and clamp limit
            limit = max(1, min(limit, 50))
            
            # Find the channel
            target_channel = await self.find_channel(channel)
            if not target_channel:
                return f"❌ Channel '{channel}' not found"
            
            # Check permissions
            if not target_channel.permissions_for(target_channel.guild.me).read_message_history:
                return f"❌ No permission to read message history in #{target_channel.name}"
            
            # Get messages
            messages = []
            async for message in target_channel.history(limit=limit):
                timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
                content = message.content or "[No text content]"
                if message.attachments:
                    content += f" [+{len(message.attachments)} attachment(s)]"
                messages.append(f"[{timestamp}] {message.author.display_name}: {content}")
            
            if not messages:
                return f"📭 No messages found in #{target_channel.name}"
            
            result = f"📋 Last {len(messages)} messages from #{target_channel.name} ({target_channel.guild.name}):\n\n"
            result += "\n".join(reversed(messages))  # Show oldest first
            return result
            
        except discord.Forbidden:
            return f"❌ No permission to read messages in {channel}"
        except Exception as e:
            return f"❌ Error getting messages: {str(e)}"
    
    async def get_channel_info(self, channel: str) -> str:
        """Get information about a Discord channel"""
        
        try:
            # Find the channel
            target_channel = await self.find_channel(channel)
            if not target_channel:
                return f"❌ Channel '{channel}' not found"
            
            # Gather channel info
            info = f"📊 Channel Information for #{target_channel.name}\n\n"
            info += f"🆔 Channel ID: {target_channel.id}\n"
            info += f"📂 Channel Type: {target_channel.type}\n"
            info += f"🏠 Server: {target_channel.guild.name} (ID: {target_channel.guild.id})\n"
            info += f"📅 Created: {target_channel.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            
            if hasattr(target_channel, 'topic') and target_channel.topic:
                info += f"📝 Topic: {target_channel.topic}\n"
            
            if hasattr(target_channel, 'category') and target_channel.category:
                info += f"📁 Category: {target_channel.category.name}\n"
            
            # Member count
            member_count = len([m for m in target_channel.guild.members if target_channel.permissions_for(m).read_messages])
            info += f"👥 Members with access: {member_count}\n"
            
            return info
            
        except Exception as e:
            return f"❌ Error getting channel info: {str(e)}"
    
    async def list_channels(self, server_name: str = "") -> str:
        """List all available channels"""
        
        try:
            result = "📋 Available Discord Channels:\n\n"
            
            for guild in self.discord_client.guilds:
                if server_name and server_name.lower() not in guild.name.lower():
                    continue
                
                result += f"🏠 **{guild.name}** (ID: {guild.id})\n"
                
                # Group channels by category
                categories = {}
                no_category = []
                
                for channel in guild.text_channels:
                    if channel.category:
                        if channel.category.name not in categories:
                            categories[channel.category.name] = []
                        categories[channel.category.name].append(channel)
                    else:
                        no_category.append(channel)
                
                # Show categorized channels
                for category_name, channels in categories.items():
                    result += f"  📁 {category_name}\n"
                    for channel in channels:
                        result += f"    #{channel.name} (ID: {channel.id})\n"
                
                # Show uncategorized channels
                if no_category:
                    result += f"  📂 No Category\n"
                    for channel in no_category:
                        result += f"    #{channel.name} (ID: {channel.id})\n"
                
                result += "\n"
            
            if not self.discord_client.guilds:
                result += "❌ Bot is not connected to any Discord servers.\n"
                result += "Please invite the bot to your server first."
            
            return result
            
        except Exception as e:
            return f"❌ Error listing channels: {str(e)}"
    
    async def start_discord(self):
        """Start Discord client"""
        try:
            await self.discord_client.start(self.bot_token)
        except discord.LoginFailure:
            print("❌ Invalid Discord bot token")
            raise
        except Exception as e:
            print(f"❌ Discord client failed: {e}")
            raise
    
    async def run_mcp_server(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )
    
    async def run(self):
        """Run both Discord client and MCP server concurrently"""
        
        print("🚀 Starting Discord MCP Server...")
        print(f"📋 Bot Token: {self.bot_token[:20]}...")
        
        # Start Discord client in background
        discord_task = asyncio.create_task(self.start_discord())
        
        # Wait for Discord to be ready
        print("⏳ Waiting for Discord client to connect...")
        try:
            await asyncio.wait_for(self.discord_ready.wait(), timeout=30.0)
        except asyncio.TimeoutError:
            print("❌ Discord client connection timeout")
            discord_task.cancel()
            return
        
        print("✅ Discord client ready! Starting MCP server...")
        
        # Now start the MCP server
        mcp_task = asyncio.create_task(self.run_mcp_server())
        
        # Run both tasks concurrently
        try:
            await asyncio.gather(discord_task, mcp_task)
        except Exception as e:
            print(f"❌ Server error: {e}")
            # Clean up
            if not discord_task.done():
                discord_task.cancel()
            if not mcp_task.done():
                mcp_task.cancel()
            raise

async def main():
    """Main entry point"""
    try:
        server = DiscordMCPServer()
        await server.run()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 