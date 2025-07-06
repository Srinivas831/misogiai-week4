# server.py
from fastmcp import FastMCP
from tools.create_meeting import create_meeting

# Create FastMCP server instance
mcp = FastMCP("Meeting Management Server")

# Register the create_meeting function as an MCP tool
@mcp.tool()
def create_meeting_tool(title: str, participants: list[str], duration: int, start_time: str) -> str:
    """Create a new meeting and save it to the database."""
    return create_meeting(title, participants, duration, start_time)

if __name__ == "__main__":
    mcp.run()
