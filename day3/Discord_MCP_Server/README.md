# Discord MCP Server

A FastMCP-based server that enables AI models to interact with Discord through the Model Context Protocol (MCP).

## 🚀 Features

- **Send Messages** - Send messages to Discord channels
- **Get Messages** - Retrieve message history from channels
- **Get Channel Info** - Fetch channel metadata and information
- **Search Messages** - Search messages with filters (coming soon)
- **Moderate Content** - Delete messages and manage users (coming soon)

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
# Install Python dependencies
python install.py
```

### 2. Configure Environment

Create a `.env` file in this directory with:

```env
# Discord Configuration
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CLIENT_ID=your_client_id_here

# MCP Server Configuration
MCP_SERVER_PORT=3000
MCP_SERVER_HOST=localhost

# Environment
NODE_ENV=development
LOG_LEVEL=debug
```

### 3. Add Bot to Discord Server

Use your OAuth URL to add the bot to your Discord server:
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=2147560448&integration_type=0&scope=bot
```

### 4. Test Connection

```bash
# Test Discord connection
python test_connection.py
```

### 5. Run the Server

```bash
# Start the MCP server
python main.py
```

## 🧪 Testing

### Available Tools

1. **send_message**
   - Send a message to a Discord channel
   - Parameters: `channel` (string), `message` (string)

2. **get_messages**
   - Get recent messages from a channel
   - Parameters: `channel` (string), `limit` (int, default: 10)

3. **get_channel_info**
   - Get channel metadata
   - Parameters: `channel` (string)

### Example Usage

Once the server is running, AI models can use these tools:

```python
# Send a message
await send_message(channel="general", message="Hello from MCP!")

# Get messages
await get_messages(channel="general", limit=5)

# Get channel info
await get_channel_info(channel="general")
```

## 📊 Logging

Logs are saved to `logs/discord_mcp.log` with rotation (daily, 7 days retention).

## 🔐 Security

- Bot token is stored in environment variables
- All operations are logged for audit purposes
- Permission checks are implemented for Discord operations

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid bot token"**
   - Check your `.env` file
   - Verify token is correct from Discord Developer Portal

2. **"Channel not found"**
   - Make sure bot is in the server
   - Check channel name spelling
   - Verify bot has permission to view the channel

3. **"No permission to send messages"**
   - Check bot permissions in Discord
   - Ensure bot has "Send Messages" permission

### Getting Help

1. Check the logs in `logs/discord_mcp.log`
2. Run `python test_connection.py` to verify setup
3. Ensure your bot has the required permissions in Discord

## 📁 Project Structure

```
Discord_MCP_Server/
├── main.py              # Main MCP server
├── install.py           # Installation script
├── test_connection.py   # Connection test
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── logs/               # Log files
└── README.md           # This file
```

## 🔄 Development

### Adding New Tools

1. Add a new tool function in `main.py`
2. Use the `@self.mcp.tool` decorator
3. Follow the existing pattern for error handling
4. Test your new tool

### Next Features

- [ ] Message search functionality
- [ ] Content moderation tools
- [ ] Authentication layer
- [ ] Multi-tenancy support
- [ ] Rate limiting
- [ ] Unit tests 