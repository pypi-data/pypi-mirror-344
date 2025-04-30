import os

from pydantic import Field

from emp_agents.providers.openai import OpenAIProviderBase
from emp_agents.providers.openai.response import Response

from .types import GrokModelType


class GrokProvider(OpenAIProviderBase[GrokModelType]):
    """
    Provider for Grok API, which follows the OpenAI API format.
    This inherits from OpenAIProvider since the APIs are compatible.
    """

    url: str = "https://api.x.ai/v1/chat/completions"

    api_key: str = Field(default_factory=lambda: os.environ["GROK_API_KEY"])
    default_model: GrokModelType = Field(default=GrokModelType.grok_2)


__all__ = [
    "GrokModelType",
    "GrokProvider",
    "Response",
]
