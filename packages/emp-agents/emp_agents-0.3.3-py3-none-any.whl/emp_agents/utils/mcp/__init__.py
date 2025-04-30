import os

from mcp import ClientSession
from mcp.client.sse import sse_client
from pydantic import AnyUrl

# Create SSE client configuration
SSE_URL = os.environ.get("MPC_SSE_URL", "http://localhost:8000/sse")


async def run() -> None:
    async with sse_client(url=SSE_URL) as (read, write):
        async with ClientSession(
            read,
            write,
        ) as session:
            # Initialize the connection
            await session.initialize()

            # List available prompts
            prompts = await session.list_prompts()
            print(f"Available prompts: {prompts}")

            # Get a prompt
            prompt = await session.get_prompt(
                "example-prompt", arguments={"name": "Alice"}
            )
            print(f"Got prompt: {prompt}")

            # List available resources
            resources = await session.list_resources()
            print(f"Available resources: {resources}")

            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {tools}")

            # Call a tool
            result = await session.call_tool("add", arguments={"a": 1, "b": 2})
            print(f"Tool result: {result}")

            # Read a resource
            content, mime_type = await session.read_resource(AnyUrl("greeting://Alice"))
            print(f"Resource content: {content}, mime type: {mime_type}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
