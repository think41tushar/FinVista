from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool import StdioServerParameters 

async def initialiseFiMCP():
    toolset = await MCPToolset.from_server_async(
        StdioServerParameters(
            command="npx",
            args=['mcp-remote','https://mcp.fi.money:8080/mcp/stream']
        )
    )

    tools = await toolset.get_tools_async()

    return tools
    