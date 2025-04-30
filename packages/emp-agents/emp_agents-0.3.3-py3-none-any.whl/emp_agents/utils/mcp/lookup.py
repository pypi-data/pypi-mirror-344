from typing import TYPE_CHECKING

from emp_agents.types.mcp import MCPClient

if TYPE_CHECKING:
    from emp_agents.models import MCPTool


class MCPUtil:
    """Set of utilities for interop between MCP and Agents SDK tools."""

    @classmethod
    async def get_all_function_tools(
        cls, clients: list["MCPClient"]
    ) -> list["MCPTool"]:
        """Get all function tools from a list of MCP servers."""
        tools = []
        tool_names: set[str] = set()
        for client in clients:
            server_tools = await cls.get_tools(client)
            server_tool_names = {tool.name for tool in server_tools}
            if len(server_tool_names & tool_names) > 0:
                raise Exception(
                    f"Duplicate tool names found across MCP servers: "
                    f"{server_tool_names & tool_names}"
                )
            tool_names.update(server_tool_names)
            tools.extend(server_tools)

        return tools

    @classmethod
    async def get_tools(cls, client: MCPClient) -> list["MCPTool"]:
        """Get all function tools from a single MCP server."""

        return await client.list_tools()
