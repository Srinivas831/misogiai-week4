# How to Connect Your Discord MCP Server to Claude

## 🚀 Quick Setup Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Environment File
Create a `.env` file in this directory:
```env
DISCORD_BOT_TOKEN=your_bot_token_here
```

### 3. Add Bot to Discord Server
**Use this URL:** https://discord.com/oauth2/authorize?client_id=1391764030192091277&permissions=2147560448&integration_type=0&scope=bot

### 4. Test Your Setup
```bash
python test_setup.py
```

### 5. Connect to Claude Desktop

#### Update Claude Configuration
**Location:** `%APPDATA%\Claude\claude_desktop_config.json`

**SECURE Configuration (Recommended):**
```json
{
  "mcpServers": {
    "discord-mcp": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "D:\\misogiai-week4\\day3\\Discord_MCP_Server"
    }
  }
}
```

**Note:** The bot token is now read from the `.env` file, not exposed in the config.

#### Restart Claude Desktop
Close and reopen Claude Desktop to load the new configuration.

## 🔧 Available Tools

Once connected, Claude can use these Discord tools:

### 1. **send_message**
- **Purpose:** Send messages to Discord channels
- **Usage:** "Send 'Hello everyone!' to the general channel"
- **Parameters:** 
  - `channel`: Channel name (without #) or channel ID
  - `message`: Message content to send

### 2. **get_messages**
- **Purpose:** Retrieve recent messages from channels
- **Usage:** "Get the last 5 messages from general"
- **Parameters:**
  - `channel`: Channel name (without #) or channel ID
  - `limit`: Number of messages (1-50, default: 10)

### 3. **get_channel_info**
- **Purpose:** Get detailed channel information
- **Usage:** "What's the info about the general channel?"
- **Parameters:**
  - `channel`: Channel name (without #) or channel ID

### 4. **list_channels**
- **Purpose:** List all available channels
- **Usage:** "Show me all Discord channels"
- **Parameters:**
  - `server_name`: Optional filter by server name

## 🧪 Testing Commands

Try these commands with Claude:

1. **"List all Discord channels"**
2. **"Send 'Hello from Claude!' to the general channel"**
3. **"Get the last 3 messages from general"**
4. **"What's the info about the general channel?"**

## 🔐 Security Features

- ✅ Bot token stored securely in `.env` file
- ✅ Permission checks for all operations
- ✅ Comprehensive error handling
- ✅ Rate limiting and input validation
- ✅ Detailed logging for debugging

## 🐛 Troubleshooting

### Common Issues

1. **"DISCORD_BOT_TOKEN not found"**
   - Create `.env` file with your bot token
   - Ensure the file is in the same directory as `mcp_server.py`

2. **"Invalid bot token"**
   - Check your bot token in Discord Developer Portal
   - Ensure no extra spaces in the `.env` file

3. **"Channel not found"**
   - Use `list_channels` tool to see available channels
   - Make sure bot is in the server and has permissions

4. **"No permission to send messages"**
   - Check bot permissions in Discord server settings
   - Ensure bot has "Send Messages" permission

5. **"MCP server not connecting"**
   - Run `python test_setup.py` to verify setup
   - Check Claude Desktop logs for errors
   - Restart Claude Desktop after config changes

### Getting Help

1. **Run the test script:** `python test_setup.py`
2. **Check Discord bot permissions** in your server
3. **Verify Claude Desktop configuration** file path and syntax
4. **Restart Claude Desktop** after making changes

## 📁 Project Structure

```
Discord_MCP_Server/
├── mcp_server.py           # Main MCP server implementation
├── test_setup.py           # Setup verification script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── instructions.md         # This file
└── README.md              # Project documentation
```

## 🎯 Next Steps

After successful setup:

1. **Test basic functionality** with the commands above
2. **Explore advanced features** like message filtering
3. **Set up multiple Discord servers** if needed
4. **Create custom workflows** combining Discord with other tools

## 🔄 Development Notes

- The server uses **stdio transport** for Claude Desktop integration
- **Proper Discord intents** are configured for message access
- **Async/await patterns** ensure responsive performance
- **Comprehensive error handling** provides clear feedback 