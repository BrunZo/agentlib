from abc import ABC
from collections.abc import Sequence
from typing import TypeVar

Message = TypeVar("Message")


class Chat(Sequence[Message], ABC):
    """An ordered, appendable sequence of messages."""

    def __init__(self, messages: list[Message] | None = None):
        self.messages: list[Message] = list(messages) if messages else []

    def __getitem__(self, index: int) -> Message:
        return self.messages[index]

    def __len__(self) -> int:
        return len(self.messages)

    def append_message(self, message: Message) -> Message:
        self.messages.append(message)
        return message

    def transcript(self) -> str:
        return "\n".join(str(m) for m in self.messages)
