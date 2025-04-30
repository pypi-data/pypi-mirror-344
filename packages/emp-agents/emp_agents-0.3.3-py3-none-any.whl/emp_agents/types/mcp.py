from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from mcp.types import Prompt, Tool
from pydantic import BaseModel, Field, PrivateAttr

if TYPE_CHECKING:
    from emp_agents.models import MCPTool


class SSEParams(BaseModel):
    url: str
    # headers: dict[str, str] | None = Field(default=None)


class MCPConnectionType(StrEnum):
    SSE = "sse"
    STDIO = "stdio"


class MCPClient(BaseModel):
    connection_type: MCPConnectionType = Field(default=MCPConnectionType.SSE)
    params: SSEParams | StdioServerParameters

    _client: ClientSession | None = PrivateAttr(default=None)

    def model_post_init(self, __context: Any) -> None:
        if self.connection_type == MCPConnectionType.SSE:
            assert isinstance(self.params, SSEParams)
        elif self.connection_type == MCPConnectionType.STDIO:
            assert isinstance(self.params, StdioServerParameters)
        else:
            raise ValueError(f"Invalid connection type: {self.connection_type}")

    # async def _create_session(self) -> ClientSession:
    #     if self._client is not None:
    #         return self._client

    #     if self.connection_type == MCPConnectionType.SSE:
    #         assert isinstance(self.params, SSEParams)
    #         read, write = await sse_client(**self.params.model_dump())
    #         session = ClientSession(read, write)
    #         await session.initialize()
    #         self._client = session
    #         return session
    #     else:
    #         assert isinstance(self.params, StdioServerParameters)
    #         read, write = await stdio_client(self.params).__aenter__()
    #         session = ClientSession(read, write)
    #         await session.initialize()
    #         self._client = session
    #         return session

    async def get_prompts(self) -> list[Prompt]:
        if self.connection_type == MCPConnectionType.SSE:
            async with sse_client(**self.params.model_dump()) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                prompts = await session.list_prompts()
        else:
            assert isinstance(self.params, StdioServerParameters)
            async with stdio_client(self.params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    prompts = await session.list_prompts()
        return prompts.prompts

    async def list_tools(self) -> list[MCPTool]:
        from emp_agents.models import MCPTool

        if self.connection_type == MCPConnectionType.SSE:
            async with sse_client(**self.params.model_dump()) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools_result = await session.list_tools()
        else:
            assert isinstance(self.params, StdioServerParameters)
            async with stdio_client(self.params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools_result = await session.list_tools()

        tools: list[Tool] = tools_result.tools
        return [
            MCPTool(
                client=self,
                name=tool.name,
                description=tool.description or "",
                parameters=tool.inputSchema.get("properties", {}),
                required=tool.inputSchema.get("required", []),
            )
            for tool in tools
        ]

    async def call_tool(self, tool_name: str, kwargs: dict[str, Any]) -> Any:
        if self.connection_type == MCPConnectionType.SSE:
            async with sse_client(**self.params.model_dump()) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(tool_name, kwargs)
        else:
            assert isinstance(self.params, StdioServerParameters)
            async with stdio_client(self.params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(tool_name, **kwargs)

        return result.content[0].text  # type: ignore
