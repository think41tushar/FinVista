import os
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# Load environment variables
load_dotenv()

async def initialiseFiMCP():
    toolset = MCPToolset(
        connection_params=StdioServerParameters(
            command='npx',
            args=[
                'mcp-remote', 
                'https://mcp.fi.money:8080/mcp/stream'
            ],
        )
    )
    tools = await toolset.get_tools()
    return tools
    