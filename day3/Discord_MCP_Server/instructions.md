# How to Connect Your Discord MCP Server to AI

## 🚀 Quick Setup

### 1. Add Bot to Discord Server
**Use this URL:** https://discord.com/oauth2/authorize?client_id=1391764030192091277&permissions=2147560448&integration_type=0&scope=bot

### 2. Test Discord Functionality
```bash
python test_direct.py
```

### 3. Connect to AI

#### Option A: Claude Desktop (Recommended)
1. Install Claude Desktop
2. Add this to your Claude config file:

**Location:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "discord-mcp-server": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "D:\\misogiai-week4\\day3\\Discord_MCP_Server"
    }
  }
}
```

#### Option B: Test with Simulation
```bash
python test_with_ai.py
```

## 🔧 Available Tools

Once connected, AI can use these tools:

1. **send_message(channel, message)**
   - Send messages to Discord channels
   - Example: "Send 'Hello' to #general"

2. **get_messages(channel, limit)**
   - Get recent messages from channels
   - Example: "Get the last 5 messages from #general"

3. **get_channel_info(channel)**
   - Get channel information
   - Example: "What's the info for #general?"

## 🧪 Testing Commands

Ask AI to:
- "Send a hello message to the general channel"
- "Get the last 3 messages from general"
- "What's the info about the general channel?"

## 🔐 Security

- Bot token is stored in .env file
- All operations are logged
- Permission checks are implemented

## 🐛 Troubleshooting

1. **Bot not in server:** Use the OAuth URL above
2. **No permission errors:** Check bot permissions in Discord
3. **Channel not found:** Make sure channel exists and bot can see it
4. **Connection issues:** Check .env file and bot token 