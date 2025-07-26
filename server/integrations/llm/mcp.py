from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

async def initialiseFiMCP():
    # Initialize the MCPToolset with the connection parameters
    toolset = MCPToolset(
        connection_params=StdioServerParameters(
            command='npx',
            args=['mcp-remote', 'https://mcp.fi.money:8080/mcp/stream'],
        )
    )

    # Get the tools from the toolset
    tools = await toolset.get_tools()

    return tools
    