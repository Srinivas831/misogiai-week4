#!/usr/bin/env python3
"""
Discord MCP Server using FastMCP 2.0
This server provides Discord integration tools for AI assistants like Claude and Cursor
"""

import asyncio
import os
from typing import Optional
from dotenv import load_dotenv

# Set FastMCP environment variables before importing
os.environ['FASTMCP_LOG_LEVEL'] = 'INFO'

import discord
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize FastMCP with proper configuration
mcp = FastMCP("Discord MCP Server")

# Discord client setup
class DiscordClient:
    def __init__(self):
        self.bot_token = os.getenv("DISCORD_BOT_TOKEN")
        if not self.bot_token:
            raise ValueError("DISCORD_BOT_TOKEN is required in .env file or environment variables")
        
        # Initialize Discord client with proper intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.guild_messages = True
        
        self.client = discord.Client(intents=intents)
        self.ready = asyncio.Event()
        self.started = False
        
        # Setup Discord events
        @self.client.event
        async def on_ready():
            print(f" Discord client ready: {self.client.user}")
            print(f" Connected to {len(self.client.guilds)} guilds")
            self.ready.set()
        
        @self.client.event
        async def on_error(event, *args, **kwargs):
            print(f" Discord error in {event}: {args}")
    
    async def ensure_ready(self):
        """Ensure Discord client is ready"""
        if not self.started:
            # Start Discord client in background
            asyncio.create_task(self.client.start(self.bot_token))
            self.started = True
        
        # Wait for Discord to be ready
        await asyncio.wait_for(self.ready.wait(), timeout=30.0)
    
    async def find_channel(self, channel_identifier: str) -> Optional[discord.TextChannel]:
        """Find a Discord channel by name or ID"""
        await self.ensure_ready()
        
        # Remove # if present
        channel_name = channel_identifier.lstrip('#')
        
        # Try to find by ID first
        if channel_name.isdigit():
            try:
                channel = self.client.get_channel(int(channel_name))
                if channel and isinstance(channel, discord.TextChannel):
                    return channel
            except ValueError:
                pass
        
        # Try to find by name
        for guild in self.client.guilds:
            for channel in guild.text_channels:
                if channel.name.lower() == channel_name.lower():
                    return channel
        
        return None

# Global Discord client instance
discord_client = DiscordClient()

# FastMCP Tools

@mcp.tool()
async def send_message(channel: str, message: str) -> str:
    """
    Send a message to a Discord channel
    
    Args:
        channel: Channel name (without #) or channel ID
        message: Message content to send
    
    Returns:
        Success or error message
    """
    try:
        # Find the channel
        target_channel = await discord_client.find_channel(channel)
        if not target_channel:
            available_channels = []
            for guild in discord_client.client.guilds:
                for ch in guild.text_channels:
                    available_channels.append(f"#{ch.name}")
            
            result = f" Channel '{channel}' not found.\n"
            result += f"Available channels: {', '.join(available_channels[:10])}"
            if len(available_channels) > 10:
                result += f" and {len(available_channels) - 10} more..."
            return result
        
        # Check permissions
        if not target_channel.permissions_for(target_channel.guild.me).send_messages:
            return f" No permission to send messages in #{target_channel.name}"
        
        # Send the message
        sent_message = await target_channel.send(message)
        return f" Message sent to #{target_channel.name} in {target_channel.guild.name} (Message ID: {sent_message.id})"
        
    except asyncio.TimeoutError:
        return "Discord client not ready (timeout)"
    except discord.Forbidden:
        return f" No permission to send messages in {channel}"
    except discord.HTTPException as e:
        return f" Discord API error: {str(e)}"
    except Exception as e:
        return f" Error sending message: {str(e)}"

@mcp.tool()
async def get_messages(channel: str, limit: int = 10) -> str:
    """
    Get recent messages from a Discord channel
    
    Args:
        channel: Channel name (without #) or channel ID
        limit: Number of messages to retrieve (1-50, default: 10)
    
    Returns:
        List of recent messages or error message
    """
    try:
        # Validate and clamp limit
        limit = max(1, min(limit, 50))
        
        # Find the channel
        target_channel = await discord_client.find_channel(channel)
        if not target_channel:
            return f" Channel '{channel}' not found"
        
        # Check permissions
        if not target_channel.permissions_for(target_channel.guild.me).read_message_history:
            return f" No permission to read message history in #{target_channel.name}"
        
        # Get messages
        messages = []
        async for message in target_channel.history(limit=limit):
            timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            content = message.content or "[No text content]"
            if message.attachments:
                content += f" [+{len(message.attachments)} attachment(s)]"
            messages.append(f"[{timestamp}] {message.author.display_name}: {content}")
        
        if not messages:
            return f" No messages found in #{target_channel.name}"
        
        result = f" Last {len(messages)} messages from #{target_channel.name} ({target_channel.guild.name}):\n\n"
        result += "\n".join(reversed(messages))  # Show oldest first
        return result
        
    except asyncio.TimeoutError:
        return " Discord client not ready (timeout)"
    except discord.Forbidden:
        return f" No permission to read messages in {channel}"
    except Exception as e:
        return f" Error getting messages: {str(e)}"

@mcp.tool()
async def get_channel_info(channel: str) -> str:
    """
    Get information about a Discord channel
    
    Args:
        channel: Channel name (without #) or channel ID
    
    Returns:
        Channel information or error message
    """
    try:
        # Find the channel
        target_channel = await discord_client.find_channel(channel)
        if not target_channel:
            return f" Channel '{channel}' not found"
        
        # Gather channel info
        info = f"Channel Information for #{target_channel.name}\n\n"
        info += f" Channel ID: {target_channel.id}\n"
        info += f" Channel Type: {target_channel.type}\n"
        info += f" Server: {target_channel.guild.name} (ID: {target_channel.guild.id})\n"
        info += f" Created: {target_channel.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
        
        if hasattr(target_channel, 'topic') and target_channel.topic:
            info += f" Topic: {target_channel.topic}\n"
        
        if hasattr(target_channel, 'category') and target_channel.category:
            info += f" Category: {target_channel.category.name}\n"
        
        # Member count
        member_count = len([m for m in target_channel.guild.members if target_channel.permissions_for(m).read_messages])
        info += f" Members with access: {member_count}\n"
        
        return info
        
    except asyncio.TimeoutError:
        return " Discord client not ready (timeout)"
    except Exception as e:
        return f" Error getting channel info: {str(e)}"

@mcp.tool()
async def list_channels(server_name: str = "") -> str:
    """
    List all available channels in connected Discord servers
    
    Args:
        server_name: Optional filter by server name
    
    Returns:
        List of available channels or error message
    """
    try:
        await discord_client.ensure_ready()
        
        result = " Available Discord Channels:\n\n"
        
        for guild in discord_client.client.guilds:
            if server_name and server_name.lower() not in guild.name.lower():
                continue
            
            result += f" **{guild.name}** (ID: {guild.id})\n"
            
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
                result += f"   {category_name}\n"
                for channel in channels:
                    result += f"    #{channel.name} (ID: {channel.id})\n"
            
            # Show uncategorized channels
            if no_category:
                result += f"   No Category\n"
                for channel in no_category:
                    result += f"    #{channel.name} (ID: {channel.id})\n"
            
            result += "\n"
        
        if not discord_client.client.guilds:
            result += " Bot is not connected to any Discord servers.\n"
            result += "Please invite the bot to your server first."
        
        return result
        
    except asyncio.TimeoutError:
        return " Discord client not ready (timeout)"
    except Exception as e:
        return f" Error listing channels: {str(e)}"

@mcp.tool()
async def discord_status() -> str:
    """
    Get Discord bot connection status
    
    Returns:
        Current status of Discord bot connection
    """
    try:
        if not discord_client.ready.is_set():
            return " Discord client is connecting..."
        
        client = discord_client.client
        result = f" Discord Bot Status:\n\n"
        result += f" Bot: {client.user.name}#{client.user.discriminator}\n"
        result += f" Bot ID: {client.user.id}\n"
        result += f" Connected to {len(client.guilds)} servers:\n"
        
        for guild in client.guilds:
            result += f"  • {guild.name} ({len(guild.text_channels)} channels)\n"
        
        return result
        
    except Exception as e:
        return f" Error getting Discord status: {str(e)}"

# Main function to run the server
def main():
    """Main function to run the FastMCP server"""
    print("Starting Discord FastMCP Server...")
    print(f" Bot Token: {discord_client.bot_token[:20]}...")
    
    # Run FastMCP server (this handles the event loop)
    mcp.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Server stopped by user")
    except Exception as e:
        print(f" Server error: {e}")
        import sys
        sys.exit(1) 