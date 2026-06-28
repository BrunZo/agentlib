import os
from dataclasses import asdict, dataclass, field
from typing import Literal

import httpx  # provides streaming support that requests doesn't
from dotenv import load_dotenv

from agentlib.completions.chat import Chat


@dataclass
class Message:
    role: Literal["system", "assistant", "user"]
    content: str

    def __str__(self):
        return f"{self.role}: {self.content}"


@dataclass
class Function:
    name: str
    description: str
    parameters: dict = field(default_factory=dict)  # JSON Schema object


@dataclass
class Tool:
    function: Function
    type: Literal["function"] = "function"


@dataclass
class UsageStats:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class Choice:
    index: int
    message: Message
    finish_reason: str  # "stop" | "length" | "content_filter" | "tool_calls"


@dataclass
class ChatCompletion:
    id: str
    model: str  # actual model used (may differ if routing falls back)
    created: int  # unix timestamp
    choices: list[Choice]
    usage: UsageStats

    @classmethod
    def from_dict(cls, data: dict) -> "ChatCompletion":
        return cls(
            id=data["id"],
            model=data["model"],
            created=data["created"],
            choices=[
                Choice(
                    index=c["index"],
                    message=Message(
                        role=c["message"]["role"],
                        content=c["message"]["content"],
                    ),
                    finish_reason=c["finish_reason"],
                )
                for c in data["choices"]
            ],
            usage=UsageStats(
                prompt_tokens=data["usage"]["prompt_tokens"],
                completion_tokens=data["usage"]["completion_tokens"],
                total_tokens=data["usage"]["total_tokens"],
            ),
        )

    @property
    def message(self) -> Message:
        return self.choices[0].message

    @property
    def content(self) -> str:
        return self.choices[0].message.content


class OpenRouterChat(Chat[Message]):
    def __init__(self, messages: list[Message] | None = None):
        super().__init__(messages)
        load_dotenv()
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL")
        self.tools: list[Tool] = []

    def append_tool(self, tool: Tool) -> Tool:
        self.tools.append(tool)
        return tool

    def ask_completion(self, *, timeout: float = 60.0) -> ChatCompletion:
        resp = httpx.post(
            self.url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "messages": [asdict(m) for m in self.messages],
                "tools": [asdict(t) for t in self.tools],
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        completion = ChatCompletion.from_dict(resp.json())
        self.append_message(completion.message)
        return completion
