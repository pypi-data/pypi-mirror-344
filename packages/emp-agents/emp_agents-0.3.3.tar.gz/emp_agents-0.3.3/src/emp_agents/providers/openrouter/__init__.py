import os

from pydantic import Field

from ..openai import OpenAIProviderBase
from .types import OpenRouterModelType


class OpenRouterProvider(OpenAIProviderBase[OpenRouterModelType]):
    url: str = "https://openrouter.ai/api/v1/chat/completions"

    api_key: str = Field(default_factory=lambda: os.environ["OPENROUTER_API_KEY"])
    default_model: OpenRouterModelType = Field(default=OpenRouterModelType.gpt3_5_turbo)
