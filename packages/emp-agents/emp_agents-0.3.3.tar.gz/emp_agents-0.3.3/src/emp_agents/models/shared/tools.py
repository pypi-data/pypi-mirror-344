import inspect
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Self, get_args, get_origin

from pydantic import BaseModel, Field

from emp_agents.types.mcp import MCPClient
from emp_agents.utils import FunctionSchema, get_function_schema

if TYPE_CHECKING:
    from emp_agents.agents.base import AgentBase


class Property(BaseModel):
    type: str | None = Field(default="string")
    description: str = ""
    enum: list[str] | None = None
    properties: dict[str, "Property"] | None = None
    required: list[str] | None = None
    items: "Property | None" = None


class GenericTool(BaseModel, ABC):
    """
    This converts a function to a generic tool.
    """

    strict: bool | None = None
    description: str
    name: str
    parameters: dict[str, Property]
    required: list[str]
    type: str = "object"
    additional_properties: bool = Field(default=False)

    @classmethod
    def _convert_type(cls, type):
        if type is str:
            return "string"
        elif get_origin(type) is list:
            return "array"
        elif inspect.isclass(type) and issubclass(type, Enum):
            return "enum"
        return str(type)

    @classmethod
    def _get_enum(cls, type):
        if inspect.isclass(type) and issubclass(type, Enum):
            return [x.name for x in list(type)]
        return None

    @classmethod
    def _get_items(cls, items):
        if get_origin(type) == list:
            return cls._convert_type(get_args(type)[0])
        return None

    @classmethod
    def _extract_params(cls, lines: list[str]):
        output = {}
        cur_key = ""
        for line in lines:
            split_line = line.split(":")
            if len(split_line) == 2:
                cur_key = split_line[0]
                output[cur_key] = split_line[1]
            else:
                output[cur_key] += split_line[0]
        return output

    def to_anthropic(self):
        from emp_agents.providers.anthropic.tool import Property, Tool, ToolSchema

        return Tool(
            name=self.name,
            description=self.description,
            input_schema=ToolSchema(
                type="object",
                properties={
                    key: Property(**param.model_dump(exclude_none=True))
                    for key, param in self.parameters.items()
                },
                required=self.required,
            ),
        )

    def to_grok(self):
        from emp_agents.providers.openai.tool import (
            Function,
            Parameters,
            Property,
            Tool,
        )

        return Tool(
            type="function",
            function=Function(
                description=self.description,
                name=self.name,
                parameters=Parameters(
                    properties={
                        key: Property(**param.model_dump(exclude_none=True))
                        for key, param in self.parameters.items()
                    },
                    required=self.required,
                ),
            ),
            strict=True,
        )

    def __repr__(self):
        description = self.description.strip().replace("\n", " ")[:100]
        if len(description) >= 50:
            description = description[:50] + "..."
        return f'<GenericTool name="{self.name}" description="{description}">'

    __str__ = __repr__

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        pass


class FunctionTool(GenericTool):
    func: Callable

    @classmethod
    def from_func(cls, func: Callable[..., Any]):
        description: str = func.__doc__ or ""
        schema: FunctionSchema = get_function_schema(func)
        parameters_ = {
            name: Property(
                type=type_["type"],
                description=type_["description"],
                enum=type_.get("enum"),
                properties=type_.get("properties"),  # type: ignore
                required=type_.get("required"),
                items=type_.get("items"),  # type: ignore
            )
            for name, type_ in schema["parameters"]["properties"].items()
        }

        return FunctionTool(
            description=description,
            name=schema["name"],
            parameters=parameters_,
            required=[
                key
                for key, value in inspect.signature(func).parameters.items()
                if value.default == inspect._empty
            ],
            func=func,
        )

    def execute(self, **kwargs):
        return self.func(**kwargs)

    @classmethod
    def from_agent(cls, agent: "AgentBase") -> Self:
        func = agent.answer
        description: str = agent.description
        parameters_ = {
            "question": Property(
                type="string",
                description="the question you want answered by the agent",
                enum=None,
            ),
        }
        return cls(
            description=description,
            name="answer",
            parameters=parameters_,
            required=[
                key
                for key, value in inspect.signature(func).parameters.items()
                if value.default == inspect._empty
            ],
            func=agent.answer,
        )


class MCPTool(GenericTool):
    client: MCPClient

    async def execute(self, **kwargs):
        return await self.client.call_tool(self.name, kwargs)
