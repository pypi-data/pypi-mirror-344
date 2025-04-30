import pytest

from emp_agents import AgentBase, OpenAIProvider


# Start the server
@pytest.mark.asyncio(scope="session")
@pytest.mark.skip(reason="This requires an external service to be running")
async def test_mcp():
    agent = AgentBase(
        mcp_clients=[
            "http://0.0.0.0:8000/sse",
        ],
        provider=OpenAIProvider(),
    )
    await agent.initialize_mcp_clients()
    response = await agent.answer(
        "Add 3 + 4?  Give me the tool response and nothing else"
    )
    assert response == "7"
