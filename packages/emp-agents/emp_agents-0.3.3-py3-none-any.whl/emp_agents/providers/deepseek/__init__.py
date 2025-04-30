from pydantic import Field

from ..openai import OpenAIProviderBase
from .types import DeepSeekModelType


class DeepSeekProvider(OpenAIProviderBase[DeepSeekModelType]):
    url: str = "https://api.deepseek.com/v1/chat/completions"

    default_model: DeepSeekModelType = Field(default=DeepSeekModelType.deepseek_chat)
